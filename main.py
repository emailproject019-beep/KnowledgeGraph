from web3 import Web3
from config import SOMNIA_RPC, PROVENANCE_CONTRACT, PROVENANCE_ABI

w3 = Web3(Web3.HTTPProvider(SOMNIA_RPC))
contract = w3.eth.contract(address=PROVENANCE_CONTRACT, abi=PROVENANCE_ABI)
def anchor_provenance(merkle_root, metadata_uri, wallet, private_key):
    tx = contract.functions.anchorProvenance(
        merkle_root,
        metadata_uri
    ).build_transaction({
        "from": wallet,
        "nonce": w3.eth.get_transaction_count(wallet),
        "gas": 300000,
        "gasPrice": w3.eth.gas_price
    })

    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()
anchor_provenance(root, uri, wallet, key)
tx = anchor_provenance(merkle_root, metadata_uri, wallet, private_key)
print("Anchored provenance:", tx)
