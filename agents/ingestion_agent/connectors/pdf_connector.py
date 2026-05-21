from typing import List
from ..schemas.raw_record import RawRecord


class PDFConnector:
    def __init__(self, config: dict) -> None:
        self.config = config

    def fetch(self) -> List[RawRecord]:
        """
        Fetch and normalise PDF documents into RawRecord objects.
        """
        # TODO: implement real PDF ingestion
        return []
