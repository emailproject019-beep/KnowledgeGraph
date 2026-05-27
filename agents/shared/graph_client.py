from typing import Any, Dict, List
from .logging import get_logger


class GraphClient:
    """
    Wrapper around Neo4j / JanusGraph.
    """

    def __init__(self, uri: str, user: str, password: str) -> None:
        self.uri = uri
        self.user = user
        self.password = password
        self.logger = get_logger(self.__class__.__name__)
        # TODO: initialise real driver

    def insert_triples(self, triples: List[Dict[str, Any]]) -> None:
        self.logger.info(f"Inserting {len(triples)} triples into graph.")
        # TODO: implement Cypher/Gremlin insert

    def query(self, query: str, params: Dict[str, Any] | None = None):
        self.logger.info(f"Running graph query: {query}")
        # TODO: implement query
        return []

class GraphClient:
    def __init__(self):
        self.triples = []

    def insert_triples(self, triples):
        self.triples.extend(triples)
        return True

    def get_all_triples(self):
        return self.triples
