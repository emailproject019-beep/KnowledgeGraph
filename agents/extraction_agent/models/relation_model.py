from typing import Any, Dict, List


class RelationModel:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        # TODO: load relation extraction model

    def extract_relations(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Return list of relations between entities.
        """
        # TODO: implement real relation extraction
        return []
