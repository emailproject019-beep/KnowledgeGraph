from typing import Any, Dict, Optional
from .logging import get_logger


class QueueClient:
    """
    Simple abstraction over a message queue (Kafka, Redis, SQS, etc.).
    Replace with concrete implementation later.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        # TODO: initialise real queue connection here

    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        self.logger.info(f"Publishing message to {topic}: {message}")
        # TODO: implement real publish

    def consume(self, topic: str, timeout: Optional[float] = None):
        """
        Generator yielding messages from a topic.
        """
        self.logger.info(f"Consuming from topic={topic}")
        # TODO: implement real consumption
        while False:
            yield {}

class QueueClient:
    def __init__(self, seed_records=None):
        self.records = seed_records or []

    def consume(self):
        for r in self.records:
            yield r

class QueueClient:
    """
    Minimal queue implementation for AKG Builder.
    Accepts a list of RawRecord objects and yields them one by one.
    """

    def __init__(self, seed_records=None):
        self.records = seed_records or []

    def add_record(self, record):
        """Append a new RawRecord to the queue."""
        self.records.append(record)

    def consume(self):
        """Yield records in FIFO order."""
        while self.records:
            yield self.records.pop(0)


from typing import Any, Dict, Optional
from .logging import get_logger

class QueueClient:
    """
    Abstraction over a message queue (Kafka, Redis, SQS, etc.).
    For testnet, can use in-memory implementation or Kafka.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.records = config.get("seed_records", [])

    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        self.logger.info(f"Publishing message to {topic}: {message}")
        self.records.append(message)

    def consume(self, topic: str, timeout: Optional[float] = None):
        """Generator yielding messages from a topic."""
        self.logger.info(f"Consuming from topic={topic}")
        for r in self.records:
            yield r
