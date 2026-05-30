from typing import Any, Dict, List
from .logging import get_logger
def submit_commit(self, merkle_root, metadata_uri):
    return "0xDEADBEEF"


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

from web3 import Web3
from config import SOMNIA_RPC, PROVENANCE_CONTRACT, PROVENANCE_ABI

class SomniaClient:
    def __init__(self, wallet, private_key):
        self.w3 = Web3(Web3.HTTPProvider(SOMNIA_RPC))
        self.wallet = wallet
        self.private_key = private_key
        self.contract = self.w3.eth.contract(
            address=PROVENANCE_CONTRACT,
            abi=PROVENANCE_ABI
        )

    def submit_commit(self, merkle_root, metadata_uri):
        tx = self.contract.functions.anchorProvenance(
            merkle_root,
            metadata_uri
        ).build_transaction({
            "from": self.wallet,
            "nonce": self.w3.eth.get_transaction_count(self.wallet),
            "gas": 300000,
            "gasPrice": self.w3.eth.gas_price
        })

        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()

from web3 import Web3
from config import SOMNIA_RPC, PROVENANCE_CONTRACT, PROVENANCE_ABI


class SomniaClient:
    """
    Handles on-chain provenance anchoring on Somnia L1.
    """

    def __init__(self, wallet, private_key):
        self.w3 = Web3(Web3.HTTPProvider(SOMNIA_RPC))
        if not self.w3.is_connected():
            raise RuntimeError("Could not connect to Somnia RPC")

        self.wallet = wallet
        self.private_key = private_key

        self.contract = self.w3.eth.contract(
            address=PROVENANCE_CONTRACT,
            abi=PROVENANCE_ABI
        )

    def submit_commit(self, merkle_root, metadata_uri):
        """
        Submit a provenance commit to Somnia L1.
        Returns the transaction hash.
        """

        tx = self.contract.functions.anchorProvenance(
            merkle_root,
            metadata_uri
        ).build_transaction({
            "from": self.wallet,
            "nonce": self.w3.eth.get_transaction_count(self.wallet),
            "gas": 300000,
            "gasPrice": self.w3.eth.gas_price
        })

        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)

        return tx_hash.hex()

from web3 import Web3
from config import SOMNIA_RPC, PROVENANCE_CONTRACT, PROVENANCE_ABI
import os

class SomniaClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("SOMNIA_RPC_URL")))
        self.wallet = os.getenv("WALLET_ADDRESS")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.contract = self.w3.eth.contract(
            address=PROVENANCE_CONTRACT,
            abi=PROVENANCE_ABI
        )

    def submit_commit(self, merkle_root, metadata_uri):
        try:
            tx = self.contract.functions.anchorProvenance(
                Web3.to_bytes(hexstr=merkle_root),
                metadata_uri
            ).build_transaction({
                "from": self.wallet,
                "nonce": self.w3.eth.get_transaction_count(self.wallet),
                "gas": 300000,
                "gasPrice": self.w3.eth.gas_price
            })

            signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            return tx_hash.hex()
        except Exception as e:
            print(f"Error submitting commit: {e}")
            raise
