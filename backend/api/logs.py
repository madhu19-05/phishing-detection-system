from flask import Blueprint, jsonify, request
from web3 import Web3
import json

logs_bp = Blueprint('logs', __name__)

# Connect to Ganache CLI
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Check connection
if not web3.is_connected():
    raise Exception("Failed to connect to Ganache CLI")

# Contract address and ABI
contract_address = '0x918e0E18bAEd4f294b74027D5A7909E71c18472B'
with open('../blockchain/build/contracts/PhishingLog.json') as f:
    abi = json.load(f)['abi']

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Get the default account from Ganache
default_account = web3.eth.accounts[0]

@logs_bp.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        logs = contract.functions.getLogs().call()
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logs_bp.route('/api/logs', methods=['POST'])
def add_log():
    data = request.json
    if data:
        try:
            tx_hash = contract.functions.addLog(data['content'], data['contentType'], data['timestamp']).transact({'from': default_account})
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            # Convert HexBytes to string
            tx_hash_hex = tx_hash.hex()
            receipt_dict = dict(receipt)
            receipt_dict['transactionHash'] = tx_hash_hex

            return jsonify(receipt_dict), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "No data provided"}), 400