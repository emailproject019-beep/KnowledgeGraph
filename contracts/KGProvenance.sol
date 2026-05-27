// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract KGProvenance {
    address public owner;

    struct Commit {
        uint256 timestamp;
        string merkleRoot;
        string metadataURI;
    }

    Commit[] public commits;

    event ProvenanceCommitted(
        uint256 indexed index,
        string merkleRoot,
        string metadataURI,
        uint256 timestamp
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function anchorProvenance(
        string calldata merkleRoot,
        string calldata metadataURI
    ) external onlyOwner {
        commits.push(Commit(block.timestamp, merkleRoot, metadataURI));
        emit ProvenanceCommitted(
            commits.length - 1,
            merkleRoot,
            metadataURI,
            block.timestamp
        );
    }
}

