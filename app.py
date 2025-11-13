from flask import Flask, jsonify
import json

app = Flask(__name__)

DATA_FILE = "data.txt"

@app.route('/')
def home():
    return "Welcome to new kingdom"

@app.route('/api')
def api():
    try:
        with open(DATA_FILE, "r") as file:
            saved_data = json.load(file)
        return jsonify({
            "message": "Data retrieved successfully!",
            "data": saved_data
        })
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in data file"}), 400

if __name__ == '__main__':
    app.run(debug=True)