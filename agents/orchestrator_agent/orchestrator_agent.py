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
