from typing import Any, Dict

from agents.base_agent.agent import BaseAgent
from agents.shared.queue_client import QueueClient
from agents.shared.graph_client import GraphClient
from agents.shared.somnia_client import SomniaClient
from .schemas.validated_triple import ValidatedTriple
from .rules.confidence_rules import ConfidenceRules
from .rules.duplicate_checker import DuplicateChecker
from .rules.conflict_resolver import ConflictResolver


class ValidatorAgent(BaseAgent):
    """
    Validator Agent:
    - Consumes TripleProposal
    - Applies confidence, duplicate, conflict rules
    - Emits ValidatedTriple
    - Writes batch commits to Somnia + updates graph
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.queue_client: QueueClient | None = None
        self.graph_client: GraphClient | None = None
        self.somnia_client: SomniaClient | None = None

        self.conf_rules: ConfidenceRules | None = None
        self.dup_checker: DuplicateChecker | None = None
        self.conf_resolver: ConflictResolver | None = None

    def load(self) -> None:
        self.logger.info("Loading ValidatorAgent.")
        self.queue_client = QueueClient(self.config.get("queue", {}))

        graph_cfg = self.config.get("graph", {})
        self.graph_client = GraphClient(
            uri=graph_cfg.get("uri", ""),
            user=graph_cfg.get("user", ""),
            password=graph_cfg.get("password", ""),
        )

        somnia_cfg = self.config.get("somnia", {})
        self.somnia_client = SomniaClient(
            rpc_url=somnia_cfg.get("rpc_url", ""),
            contract_address=somnia_cfg.get("contract_address", ""),
            private_key=somnia_cfg.get("private_key", ""),
        )

        self.conf_rules = ConfidenceRules(
            min_confidence=self.config.get("min_confidence", 0.7)
        )
        self.dup_checker = DuplicateChecker(self.config.get("duplicates", {}))
        self.conf_resolver = ConflictResolver(self.config.get("conflicts", {}))

    def _validate_triple(self, proposal: Dict[str, Any]) -> ValidatedTriple:
        assert self.conf_rules and self.dup_checker and self.conf_resolver

        confidence = proposal["confidence"]
        if not self.conf_rules.is_confident(confidence):
            return ValidatedTriple(
                status="rejected",
                reason="low_confidence",
                subject=proposal["subject"],
                predicate=proposal["predicate"],
                object=proposal["object"],
                timestamp=proposal["timestamp"],
                provenance=proposal["provenance"],
                confidence=confidence,
            )

        if self.dup_checker.is_duplicate(proposal):
            return ValidatedTriple(
                status="rejected",
                reason="duplicate",
                subject=proposal["subject"],
                predicate=proposal["predicate"],
                object=proposal["object"],
                timestamp=proposal["timestamp"],
                provenance=proposal["provenance"],
                confidence=confidence,
            )

        resolved = self.conf_resolver.resolve(proposal)

        return ValidatedTriple(
            status="approved",
            reason=None,
            subject=resolved["subject"],
            predicate=resolved["predicate"],
            object=resolved["object"],
            timestamp=resolved["timestamp"],
            provenance=resolved["provenance"],
            confidence=resolved["confidence"],
        )

    def _commit_batch(self, approved_triples: list[ValidatedTriple]) -> None:
        if not approved_triples:
            return

        assert self.graph_client and self.somnia_client

        triples_payload = [
            {
                "subject": t.subject,
                "predicate": t.predicate,
                "object": t.object,
                "timestamp": t.timestamp,
                "provenance": t.provenance,
                "confidence": t.confidence,
            }
            for t in approved_triples
        ]

        # 1) Write to graph
        self.graph_client.insert_triples(triples_payload)

        # 2) Compute Merkle root (placeholder)
        merkle_root = "MERKLE_ROOT_PLACEHOLDER"

        # 3) Anchor on Somnia
        metadata = {"count": len(approved_triples)}
        commit_id = self.somnia_client.submit_commit(merkle_root, metadata)
        self.logger.info(f"Anchored batch to Somnia: commit_id={commit_id}")

    def run(self) -> None:
        self.logger.info("Starting ValidatorAgent loop.")
        assert self.queue_client is not None

        batch: list[ValidatedTriple] = []
        batch_size = self.config.get("batch_size", 50)

        for proposal in self.queue_client.consume(topic="triple_proposals"):
            try:
                vt = self._validate_triple(proposal)
                if vt.status == "approved":
                    batch.append(vt)

                if len(batch) >= batch_size:
                    self._commit_batch(batch)
                    batch.clear()
            except Exception as e:
                self.logger.exception(f"Error validating triple: {e}")
