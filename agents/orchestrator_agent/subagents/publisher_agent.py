from typing import Any, Dict
from agents.shared.queue_client import QueueClient


class PublisherAgent:
    def __init__(self, queue_client: QueueClient, config: Dict[str, Any]) -> None:
        self.queue_client = queue_client
        self.config = config

    def publish_insight(self, insight: Dict[str, Any]) -> None:
        topic = self.config.get("topic", "insights")
        self.queue_client.publish(topic=topic, message=insight)
