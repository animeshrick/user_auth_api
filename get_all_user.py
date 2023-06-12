from flask import Flask, jsonify
from pymongo import MongoClient


app = Flask(__name__)

# Connection configuration
host = 'localhost'
port = 27017
database = 'ecomm'

# Create a connection to MongoDB
client = MongoClient(host, port)
db = client[database]

user_collection_name = 'user'

collection = db[user_collection_name]

# --------- get all users ---------------
@app.route('/api/v1/users', methods=['GET'])
def users():

    users = collection.find()
    # user_list = [user for user in users]
    # return jsonify(user_list)
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        user_list.append(user)
    return jsonify(user_list)



if __name__ == '__main__':
    app.run(port=5001, debug=True)