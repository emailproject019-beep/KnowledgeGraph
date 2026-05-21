from typing import List
from ..schemas.raw_record import RawRecord


class WebhookConnector:
    def __init__(self, config: dict) -> None:
        self.config = config

    def fetch(self) -> List[RawRecord]:
        """
        Fetch webhook events (or read from a buffer) and normalise.
        """
        # TODO: implement real webhook ingestion
        return []
