from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask import send_from_directory
from collections import deque
import random

app = Flask(__name__)

log_data = deque(maxlen=50)

motivational_messages = [
    "Nice! You're safe and secure. 🔐",
    "You're on top of it! 👍",
    "Well done, peace of mind activated. 🌟",
    "Another day, another lock. 💪",
    "Secure and sorted. ✅"
]

@app.route('/')
def home():
    last = log_data[-1] if log_data else None
    return render_template('index.html', last_locked=last, history=list(log_data))

@app.route('/log', methods=['POST'])
def log_lock():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_data.append(timestamp)
    message = random.choice(motivational_messages)
    return jsonify({"success": True, "timestamp": timestamp, "message": message})

@app.route('/undo', methods=['POST'])
def undo_last():
    if log_data:
        removed = log_data.pop()
        return jsonify({"success": True, "removed": removed})
    return jsonify({"success": False, "message": "No logs to undo"})

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@app.route('/manual', methods=['POST'])
def manual_log():
    timestamp = request.json.get("timestamp")
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        log_data.append(timestamp)
        return jsonify({"success": True, "timestamp": timestamp})
    except ValueError:
        return jsonify({"success": False, "message": "Invalid timestamp format"})
if __name__ == '__main__':
    app.run(debug=True)