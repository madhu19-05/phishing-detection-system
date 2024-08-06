// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PhishingLog {
    struct LogEntry {
        string content;
        string contentType;
        uint timestamp;
    }

    LogEntry[] public logs;

    function addLog(string memory _content, string memory _contentType, uint _timestamp) public {
        logs.push(LogEntry({
            content: _content,
            contentType: _contentType,
            timestamp: _timestamp
        }));
    }

    function getLogs() public view returns (LogEntry[] memory) {
        return logs;
    }
}
