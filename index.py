from flask import Flask,render_template,request,redirect, url_for
from dotenv import load_dotenv
import pymongo
from pymongo.errors import PyMongoError
import os 



load_dotenv() 

MONGO_URL = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_URL)
db = client.cluster0
collection = db['flask']
app = Flask(__name__) 

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html',status=request.args.get('status'))  

@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    
    try:
      inserted = collection.insert_one(data)
      if inserted.acknowledged: 
        return "Registration Successful!" 
      else:
        message = "Registration failed!" 
        return redirect(url_for('home', status=message)) 
    except PyMongoError as e:
        message = f"Database error: {str(e)}"
        return redirect(url_for('home', status=message))
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        return redirect(url_for('home', status=message))
if __name__ == '__main__':
    app.run(debug=True)