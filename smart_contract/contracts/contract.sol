// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataProvenance {
    struct DataRecord {
        bytes32 dataHash;
        uint256 timestamp;
        address owner;
    }

    mapping(bytes32 => DataRecord) public records;

    function storeHash(bytes32 _hash) external {
        require(records[_hash].timestamp == 0, "Hash already exists");
        records[_hash] = DataRecord(_hash, block.timestamp, msg.sender);
    }

    function verifyHash(bytes32 _hash) external view returns (bool) {
        return records[_hash].timestamp != 0;
    }
}
