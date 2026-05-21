from typing import Dict


class ConfidenceRules:
    def __init__(self, min_confidence: float = 0.7) -> None:
        self.min_confidence = min_confidence

    def is_confident(self, confidence: float) -> bool:
        return confidence >= self.min_confidence
