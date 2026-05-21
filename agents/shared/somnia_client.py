from typing import Any, Dict, List
from .logging import get_logger


class SomniaClient:
    """
    Client for interacting with Somnia Agentic L1.

    Responsibilities:
    - Submit commit hashes / Merkle roots
    - Fetch provenance records
    """

    def __init__(self, rpc_url: str, contract_address: str, private_key: str) -> None:
        self.rpc_url = rpc_url
        self.contract_address = contract_address
        self.private_key = private_key
        self.logger = get_logger(self.__class__.__name__)
        # TODO: initialise web3 / SDK

    def submit_commit(self, merkle_root: str, metadata: Dict[str, Any]) -> str:
        """
        Submit a commit to Somnia. Returns tx hash or commit ID.
        """
        self.logger.info(
            f"Submitting commit to Somnia: merkle_root={merkle_root}, metadata={metadata}"
        )
        # TODO: implement on-chain call
        return "0xDEADBEEF"

    def get_provenance(self, commit_id: str) -> Dict[str, Any]:
        self.logger.info(f"Fetching provenance for commit_id={commit_id}")
        # TODO: implement on-chain read
        return {}
