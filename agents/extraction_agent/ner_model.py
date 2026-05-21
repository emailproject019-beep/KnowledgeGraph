from typing import Any, Dict, List


class NERModel:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        # TODO: load spaCy / HF model

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Return list of entities with types and spans.
        """
        # TODO: implement real NER
        return []
