# backend/api/app.py
import json
from flask import Flask, request, jsonify
import joblib
import pandas as pd
from web3 import Web3
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Load the model
model = joblib.load('models/phishing_model.pkl')

# Set up Web3 connection
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Update with your provider URL
contract_address = '0xe641ccd0435EF2d4ea2eeF977a415340B81cbbF5'  # Replace with your deployed contract address
with open('../blockchain/build/contracts/PhishingLog.json') as f:
    abi = json.load(f)['abi']

contract = w3.eth.contract(address=contract_address, abi=abi)
def test_contract():
    try:
        # Example function call (replace with actual function names and parameters)
        tx_hash = contract.functions.exampleFunction().transact({
            'from': w3.eth.default_account
        })
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt: {dict(receipt)}")
    except Exception as e:
        print(f"Error: {e}")

test_contract()

# Set up MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/') 
db = mongo_client['phishing_detection']  # Database name
logs_collection = db['logs']  # Collection name
test_doc = {'type': 'phishing_url', 'content': 'http://example.com', 'timestamp': '2024-08-06T12:00:00', 'is_phishing': False}
result = logs_collection.insert_one(test_doc)
print(f"Inserted document ID: {result.inserted_id}")

def extract_features(df, type_):
    features = pd.DataFrame()
    if type_ == 'email':
        features['length'] = df['email_text'].apply(len)
    elif type_ == 'url':
        features['length'] = df['url'].apply(len)
    return features

@app.route('/api/logs', methods=['POST'])
def add_log():
    data = request.json
    content_type = data.get('type')
    content = data.get('content')
    timestamp = data.get('timestamp')

    if content_type not in ['phishing_url', 'phishing_email']:
        return jsonify({"error": "Invalid content type"}), 400

    if not content or not timestamp:
        return jsonify({"error": "Content and timestamp are required"}), 400

    # Predict if the content is phishing
    df = pd.DataFrame([{'email_text': content}] if content_type == 'phishing_email' else [{'url': content}])
    features = extract_features(df, 'email' if content_type == 'phishing_email' else 'url')
    prediction = model.predict(features)
    is_phishing = prediction[0] == 1

    # Store log in MongoDB
    log_entry = {
        'type': content_type,
        'content': content,
        'timestamp': datetime.fromisoformat(timestamp),  # Convert to datetime
        'is_phishing': is_phishing
    }
    logs_collection.insert_one(log_entry)

    # Add log to the blockchain
    tx_hash = contract.functions.addLog(content, content_type, int(timestamp)).transact({
        'from': w3.eth.default_account
    })
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return jsonify({
        "type": content_type,
        "content": content,
        "timestamp": timestamp,
        "is_phishing": is_phishing,
        "transaction_receipt": dict(receipt)
    })

if __name__ == '__main__':
    app.run(debug=True)
