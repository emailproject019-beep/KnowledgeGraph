from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class TripleProposal:
    subject: str
    predicate: str
    object: str
    timestamp: str
    provenance: Dict[str, Any]
    confidence: float
