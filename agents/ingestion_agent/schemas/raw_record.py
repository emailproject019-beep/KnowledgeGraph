from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RawRecord:
    source_type: str          # e.g. "pdf", "webhook", "csv"
    source_id: str            # unique identifier
    payload: Dict[str, Any]   # normalised content
    metadata: Dict[str, Any]  # timestamps, origin, etc.
