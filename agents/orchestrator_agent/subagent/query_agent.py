from typing import Any, Dict, List
from agents.shared.graph_client import GraphClient


class QueryAgent:
    def __init__(self, graph_client: GraphClient) -> None:
        self.graph_client = graph_client

    def get_context(self, query: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        return self.graph_client.query(query, params or {})
