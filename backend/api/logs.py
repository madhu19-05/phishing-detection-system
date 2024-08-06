from flask import Blueprint, jsonify, request, current_app

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/api/logs', methods=['GET'])
def get_logs():
    db = current_app.config['db']
    logs = list(db.detection_logs.find({}, {"_id": 0}))  # Fetch logs without MongoDB ID field
    return jsonify(logs)

@logs_bp.route('/api/logs', methods=['POST'])
def add_log():
    db = current_app.config['db']
    data = request.json
    if data:
        db.detection_logs.insert_one(data)
        return jsonify({"message": "Log added successfully"}), 201
    else:
        return jsonify({"message": "No data provided"}), 400
