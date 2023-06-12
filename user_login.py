from flask import Flask, request, jsonify
from werkzeug.security import  check_password_hash
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


users_collection = db[user_collection_name]


@app.route('/api/v1/login/', methods=['POST'])
def login():
    data = request.json

    email_phone = data.get('email_phone')
    password = data.get('password')


    # Retrieve the user from the database based on the email
    user_on_email = users_collection.find_one({'email': email_phone})

    # Retrieve the user from the database based on the phone
    user_on_phone = users_collection.find_one({'phone': email_phone})

    if user_on_email and check_password_hash(user_on_email['password'], password):

        del user_on_email['password']  # Remove password field from the response
        print('user_on_email = ',str(user_on_email))
        return jsonify({'message':'Login successful using email'})

    elif user_on_phone and check_password_hash(user_on_phone['password'], password):

        # del user_on_phone['password']
        print('user_on_phone = ',str(user_on_phone))
        print('psw = ',str(check_password_hash(user_on_email['password'], password)))
        return jsonify({'message':'Login successful using phone no'})
    
    else:
        # Invalid login credentials
        return jsonify({'message': 'Invalid email/phone or password'}), 401


# --------- get all users ---------------
@app.route('/api/v1/users', methods=['GET'])
def users():
    collection = db[user_collection_name]
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
