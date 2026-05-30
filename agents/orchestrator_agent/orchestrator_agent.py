from typing import Any, Dict, List

from agents.base_agent.agent import BaseAgent
from agents.shared.queue_client import QueueClient
from agents.shared.graph_client import GraphClient
from .subagents.query_agent import QueryAgent
from .subagents.reasoning_agent import ReasoningAgent
from .subagents.summariser_agent import SummariserAgent
from .subagents.publisher_agent import PublisherAgent


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent:
    - Periodically queries KG
    - Uses ReasoningAgent to plan actions
    - Uses SummariserAgent to generate insights
    - Uses PublisherAgent to push updates
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.queue_client: QueueClient | None = None
        self.graph_client: GraphClient | None = None

        self.query_agent: QueryAgent | None = None
        self.reasoning_agent: ReasoningAgent | None = None
        self.summariser_agent: SummariserAgent | None = None
        self.publisher_agent: PublisherAgent | None = None

    def load(self) -> None:
        self.logger.info("Loading OrchestratorAgent.")
        self.queue_client = QueueClient(self.config.get("queue", {}))

        graph_cfg = self.config.get("graph", {})
        self.graph_client = GraphClient(
            uri=graph_cfg.get("uri", ""),
            user=graph_cfg.get("user", ""),
            password=graph_cfg.get("password", ""),
        )

        assert self.graph_client and self.queue_client

        self.query_agent = QueryAgent(self.graph_client)
        self.reasoning_agent = ReasoningAgent(self.config.get("reasoning", {}))
        self.summariser_agent = SummariserAgent(self.config.get("summariser", {}))
        self.publisher_agent = PublisherAgent(
            queue_client=self.queue_client,
            config=self.config.get("publisher", {}),
        )

    def run(self) -> None:
        import time

        self.logger.info("Starting OrchestratorAgent loop.")
        assert (
            self.query_agent
            and self.reasoning_agent
            and self.summariser_agent
            and self.publisher_agent
        )

        query_str = self.config.get("query", "MATCH (n) RETURN n LIMIT 10")
        interval = self.config.get("interval_seconds", 30)

        try:
            while True:
                context = self.query_agent.get_context(query_str)
                actions = self.reasoning_agent.plan_actions(context)
                summary = self.summariser_agent.summarise(context)

                insight = {
                    "summary": summary,
                    "actions": actions,
                }
                self.publisher_agent.publish_insight(insight)

                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("OrchestratorAgent interrupted.")
            self.shutdown()
for raw in self.queue.consume():
    proposal = self.extraction_agent.run(raw)
    validated = self.validator_agent.run(proposal)

    self.graph.insert_triples(validated.triples)

    merkle_root = validated.merkle_root
    metadata_uri = validated.metadata_uri

    tx = self.somnia.submit_commit(merkle_root, metadata_uri)
    print("Anchored:", tx)

from agents.shared.merkle import merkle_root

...

validated = self.validator_agent.run(proposal)
triples = validated.triples

root = merkle_root(triples)
tx = self.somnia.submit_commit(root, validated.metadata_uri)

print("Anchored provenance:", tx)



from typing import Optional, List, Any

from agents.base_agent import BaseAgent
from agents.shared.queue_client import QueueClient
from agents.shared.graph_client import GraphClient
from agents.shared.somnia_client import SomniaClient
from agents.shared.merkle import merkle_root


class OrchestratorAgent(BaseAgent):
    """
    Orchestrates the full AKG pipeline:

    RawRecord
      -> ExtractionAgent (triple proposal)
      -> ValidatorAgent (validated triples)
      -> GraphClient.insert_triples()
      -> Merkle root over triples
      -> SomniaClient.submit_commit()
    """

    def __init__(
        self,
        ingestion_agent,
        extraction_agent,
        validator_agent,
        wallet: str,
        private_key: str,
        seed_records: Optional[List[Any]] = None,
    ):
        super().__init__(name="orchestrator_agent")

        # Core components
        self.queue = QueueClient(seed_records=seed_records)
        self.graph = GraphClient()
        self.somnia = SomniaClient(wallet=wallet, private_key=private_key)

        # Other agents in the system
        self.ingestion_agent = ingestion_agent
        self.extraction_agent = extraction_agent
        self.validator_agent = validator_agent

        self._running = False

    # -------------------------
    # BaseAgent lifecycle
    # -------------------------
    def load(self):
        self._running = True
        self.log("Orchestrator loaded")

    def shutdown(self):
        self._running = False
        self.log("Orchestrator shutting down")

    # -------------------------
    # Core pipeline
    # -------------------------
    def run(self):
        """
        Main orchestration loop.
        Consumes RawRecords from QueueClient and drives them through the pipeline.
        """
        self.log("Starting orchestration loop")

        for raw_record in self.queue.consume():
            if not self._running:
                break

            self.log(f"Processing RawRecord: {raw_record}")

            # 1. Ingestion (optional pre-processing)
            ingested = self.ingestion_agent.run(raw_record)
            self.log("Ingestion complete")

            # 2. Extraction -> TripleProposal
            triple_proposal = self.extraction_agent.run(ingested)
            triples = getattr(triple_proposal, "triples", None)
            if not triples:
                self.log("No triples extracted; skipping record")
                continue
            self.log(f"Extracted {len(triples)} triples")

            # 3. Validation -> ValidatedTriple
            validated = self.validator_agent.run(triple_proposal)
            validated_triples = getattr(validated, "triples", None)
            metadata_uri = getattr(validated, "metadata_uri", "")

            if not validated_triples:
                self.log("No validated triples; skipping record")
                continue
            self.log(f"Validated {len(validated_triples)} triples")

            # 4. Insert into graph
            self.graph.insert_triples(validated_triples)
            self.log(
                f"Graph now contains {self.graph.count()} triples in total"
            )

            # 5. Compute Merkle root over validated triples
            root = merkle_root(validated_triples)
            self.log(f"Computed Merkle root: {root}")

            # 6. Anchor provenance on Somnia
            tx_hash = self.somnia.submit_commit(root, metadata_uri)
            self.log(f"Anchored provenance on Somnia: tx={tx_hash}")

        self.log("Orchestration loop finished")


# Optional: simple entrypoint for local runs
if __name__ == "__main__":
    from agents.ingestion_agent import IngestionAgent
    from agents.extraction_agent import ExtractionAgent
    from agents.validator_agent import ValidatorAgent

    # TODO: replace with real wallet + key (from config/env)
    WALLET_ADDRESS = "0xYOUR_WALLET"
    PRIVATE_KEY = "0xYOUR_PRIVATE_KEY"

    # Example seed records (replace with real RawRecord objects)
    seed_records = [
        {"id": 1, "text": "Alice knows Bob"},
        {"id": 2, "text": "Bob works at ACME"},
    ]

    ingestion = IngestionAgent()
    extraction = ExtractionAgent()
    validator = ValidatorAgent()

    orchestrator = OrchestratorAgent(
        ingestion_agent=ingestion,
        extraction_agent=extraction,
        validator_agent=validator,
        wallet=WALLET_ADDRESS,
        private_key=PRIVATE_KEY,
        seed_records=seed_records,
    )

    orchestrator.load()
    orchestrator.run()
    orchestrator.shutdown()
