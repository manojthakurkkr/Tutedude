from flask import Flask, jsonify,request
import json
from dotenv import load_dotenv
import pymongo
from pymongo.errors import PyMongoError
import os 


load_dotenv() 

MONGO_URL = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_URL)
db = client.cluster0
collection = db['todo']

app = Flask(__name__)

DATA_FILE = "data.txt"

@app.route('/')
def home():
    return "Welcome to new kingdom"


@app.route('/submittodoitem',methods=['POST'])   
def submit_todo_item():
    name = request.json.get('itemName')
    description = request.json.get('itemDescription')
    todo_item = {
        "itemName": name,
        "itemDescription": description
    }
    inserted = collection.insert_one(todo_item)
    if inserted.acknowledged: 
        return "to do saved successfully!" 
    else:
        message = "something went wrong!" 
    return redirect(url_for('home', status=message)) 

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