import React, { useEffect, useState } from 'react';
import Web3 from 'web3';

const BlockchainLog = () => {
    const [logs, setLogs] = useState([]);
    const [web3, setWeb3] = useState(null);
    const [contract, setContract] = useState(null);

    const contractAddress = '0xff71b34D6b03f3e07AACCF8eEDB39f8c3ECa3086';  
    const abi = [  {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "logs",
      "outputs": [
        {
          "internalType": "string",
          "name": "content",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "contentType",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_content",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_contentType",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "addLog",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getLogs",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "content",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "contentType",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            }
          ],
          "internalType": "struct PhishingLog.LogEntry[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    }];  

    useEffect(() => {
        loadWeb3();
    }, []);

    const loadWeb3 = async () => {
        const web3Instance = new Web3(Web3.givenProvider || 'http://127.0.0.1:8545');
        const contractInstance = new web3Instance.eth.Contract(abi, contractAddress);
        setWeb3(web3Instance);
        setContract(contractInstance);
    };

    const fetchLogs = async () => {
        if (contract) {
            const logs = await contract.methods.getLogs().call();
            setLogs(logs);
        }
    };

    return (
        <div>
            <button onClick={fetchLogs}>Fetch Logs</button>
            <ul>
                {logs.map((log, index) => (
                    <li key={index}>
                        {log.contentType}: {log.content} at {new Date(log.timestamp * 1000).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default BlockchainLog;
