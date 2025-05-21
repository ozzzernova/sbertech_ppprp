from flask import Flask, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler
import socket

app = Flask(__name__)

LOG_DIR = '/app/logs'
LOG_FILE = '/app/logs/app.log'

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

handler = RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/status', methods=["GET"])
def status():
    return jsonify({
        "status": "ok"
    })

@app.route('/log', methods=['POST'])
def logs():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No data in message"}), 400

    app.logger.info(f"Message: {data['message']}")
    return jsonify({
        "status": "logged",
    }), 200

@app.route('/', methods=["GET"])
def hello():
    return f"Welcome from {socket.gethostname()}!"

@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.read()
        return logs
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)