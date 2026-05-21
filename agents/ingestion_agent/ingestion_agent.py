import time
from typing import Any, Dict, List

from agents.base_agent.agent import BaseAgent
from agents.shared.queue_client import QueueClient
from .schemas.raw_record import RawRecord
from .connectors.pdf_connector import PDFConnector
from .connectors.webhook_connector import WebhookConnector
from .connectors.csv_connector import CSVConnector


class IngestionAgent(BaseAgent):
    """
    Ingestion Agent:
    - Connects to multiple data sources
    - Normalises into RawRecord
    - Publishes to ingestion queue
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.queue_client: QueueClient | None = None
        self.connectors: List[Any] = []

    def load(self) -> None:
        self.logger.info("Loading IngestionAgent.")
        self.queue_client = QueueClient(self.config.get("queue", {}))

        # Initialise connectors based on config
        sources_cfg = self.config.get("sources", {})
        if "pdf" in sources_cfg:
            self.connectors.append(PDFConnector(sources_cfg["pdf"]))
        if "webhook" in sources_cfg:
            self.connectors.append(WebhookConnector(sources_cfg["webhook"]))
        if "csv" in sources_cfg:
            self.connectors.append(CSVConnector(sources_cfg["csv"]))

    def _emit_raw_record(self, record: RawRecord) -> None:
        assert self.queue_client is not None
        message = {
            "source_type": record.source_type,
            "source_id": record.source_id,
            "payload": record.payload,
            "metadata": record.metadata,
        }
        self.queue_client.publish(topic="raw_records", message=message)

    def run(self) -> None:
        self.logger.info("Starting IngestionAgent loop.")
        poll_interval = self.config.get("poll_interval_seconds", 10)

        try:
            while True:
                for connector in self.connectors:
                    records: List[RawRecord] = connector.fetch()
                    for record in records:
                        self._emit_raw_record(record)
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            self.logger.info("IngestionAgent interrupted.")
            self.shutdown()
