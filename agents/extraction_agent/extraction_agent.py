from typing import Any, Dict, List

from agents.base_agent.agent import BaseAgent
from agents.shared.queue_client import QueueClient
from .schemas.triple_proposal import TripleProposal
from .models.ner_model import NERModel
from .models.relation_model import RelationModel
from .models.temporal_tagger import TemporalTagger


class ExtractionAgent(BaseAgent):
    """
    Extraction Agent:
    - Consumes RawRecord messages
    - Runs NER, relation extraction, temporal tagging
    - Emits TripleProposal messages
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.queue_client: QueueClient | None = None
        self.ner_model: NERModel | None = None
        self.relation_model: RelationModel | None = None
        self.temporal_tagger: TemporalTagger | None = None

    def load(self) -> None:
        self.logger.info("Loading ExtractionAgent.")
        self.queue_client = QueueClient(self.config.get("queue", {}))
        self.ner_model = NERModel(self.config.get("ner", {}))
        self.relation_model = RelationModel(self.config.get("relation", {}))
        self.temporal_tagger = TemporalTagger(self.config.get("temporal", {}))

    def _build_triple_proposals(self, raw: Dict[str, Any]) -> List[TripleProposal]:
        assert self.ner_model and self.relation_model and self.temporal_tagger

        text = raw["payload"].get("text", "")
        metadata = raw.get("metadata", {})

        entities = self.ner_model.extract_entities(text)
        relations = self.relation_model.extract_relations(text, entities)
        timestamp = self.temporal_tagger.infer_timestamp(text, metadata)

        proposals: List[TripleProposal] = []
        for rel in relations:
            proposals.append(
                TripleProposal(
                    subject=rel["subject"],
                    predicate=rel["predicate"],
                    object=rel["object"],
                    timestamp=timestamp,
                    provenance={
                        "source_type": raw["source_type"],
                        "source_id": raw["source_id"],
                    },
                    confidence=rel.get("confidence", 0.8),
                )
            )
        return proposals

    def _emit_triple_proposal(self, proposal: TripleProposal) -> None:
        assert self.queue_client is not None
        message = {
            "subject": proposal.subject,
            "predicate": proposal.predicate,
            "object": proposal.object,
            "timestamp": proposal.timestamp,
            "provenance": proposal.provenance,
            "confidence": proposal.confidence,
        }
        self.queue_client.publish(topic="triple_proposals", message=message)

    def run(self) -> None:
        self.logger.info("Starting ExtractionAgent loop.")
        assert self.queue_client is not None

        for raw in self.queue_client.consume(topic="raw_records"):
            try:
                proposals = self._build_triple_proposals(raw)
                for p in proposals:
                    self._emit_triple_proposal(p)
            except Exception as e:
                self.logger.exception(f"Error processing raw record: {e}")
