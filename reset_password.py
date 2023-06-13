from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash



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

def validate_password(password):
    # Define password rules
    min_length = 8
    requires_uppercase = True
    requires_lowercase = True
    requires_digit = True
    requires_special = True

    if len(password) < min_length:
        return (
            'Password must be at least {} characters long.'.format(min_length))

    elif requires_uppercase and not any(char.isupper() for char in password):
        return ('Password must contain at least one uppercase letter.')

    elif requires_lowercase and not any(char.islower() for char in password):
        return ('Password must contain at least one lowercase letter.')

    elif requires_digit and not any(char.isdigit() for char in password):
        return ('Password must contain at least one digit.')

    elif requires_special and not any(not char.isalnum() for char in password):
        return ('Password must contain at least one special character.')

    else:
        return 'True'
    

@app.route('/api/v1/resetpassword',methods = ['POST'])
def reset_password():
    data = request.json
    
    # current_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_id = data.get('user_id') #obj id == user id
    new_password = data.get('new_pass')
    conf_password = data.get('conf_pass')
    
    if new_password != conf_password:
        return jsonify({'message':"Your password not matched"})
    
    elif validate_password(new_password) != "True" and validate_password(conf_password) != "True":
        return jsonify({'err': validate_password(password)})
    
    else:
        hide_password = generate_password_hash(new_password)
        a = collection.update_one({'_id': user_id}, {'$set': {'password': hide_password}})   
        print('update db = ',hide_password)
        return jsonify({'message':"Your password has been reset. Please try to login."})
    
    
if __name__ == '__main__':
    app.run(port=5001, debug=True)