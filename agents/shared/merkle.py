import hashlib
from typing import List


def sha256(data: bytes) -> bytes:
    """Return SHA-256 digest of input bytes."""
    return hashlib.sha256(data).digest()


def hash_leaf(triple: tuple) -> bytes:
    """
    Hash a triple (subject, predicate, object) into a leaf node.
    Triple is converted to a canonical UTF-8 string.
    """
    s, p, o = triple
    canonical = f"{s}|{p}|{o}".encode("utf-8")
    return sha256(canonical)


def merkle_parent(left: bytes, right: bytes) -> bytes:
    """Hash two children to form a parent node."""
    return sha256(left + right)


def merkle_layer(nodes: List[bytes]) -> List[bytes]:
    """
    Build the next layer of the Merkle tree.
    If odd number of nodes, duplicate the last one.
    """
    if len(nodes) == 1:
        return nodes

    new_layer = []
    for i in range(0, len(nodes), 2):
        left = nodes[i]
        right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
        new_layer.append(merkle_parent(left, right))

    return new_layer


def merkle_root(triples: List[tuple]) -> str:
    """
    Compute the Merkle root for a list of triples.
    Returns a hex string.
    """
    if not triples:
        raise ValueError("Cannot compute Merkle root of empty triple list")

    # Step 1: hash each triple into a leaf
    leaves = [hash_leaf(t) for t in triples]

    # Step 2: build tree until one root remains
    layer = leaves
    while len(layer) > 1:
        layer = merkle_layer(layer)

    # Step 3: return hex-encoded root
    return layer[0].hex()
