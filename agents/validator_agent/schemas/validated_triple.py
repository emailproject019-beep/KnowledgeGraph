from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ValidatedTriple:
    subject: str
    predicate: str
    object: str
    timestamp: str
    provenance: Dict[str, Any]
    confidence: float
    status: str          # "approved" | "rejected"
    reason: str | None
