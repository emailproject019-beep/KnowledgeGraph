from typing import Any, Dict, List


class SummariserAgent:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def summarise(self, context: List[Dict[str, Any]]) -> str:
        """
        Produce a human-readable summary of the KG context.
        """
        # TODO: implement real summarisation
        return f"Summary of {len(context)} graph records."
