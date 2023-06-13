from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)

# Connection configuration
host = 'localhost'
port = 27017
database = 'ecomm'

# Create a connection to MongoDB
client = MongoClient(host, port)
db = client[database]

user_collection_name = 'user'


# def onSuccess(message):
#     return jsonify({'status': "Ok", "message": str(message)}),


# def onError(message):
#     return jsonify({'status': "Failed", "message": message}),

# email validation


def validate_email_address(email):
    try:
        valid = validate_email(email)
        return 'True'
    except EmailNotValidError as e:
        return str(e)

# password validation


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
    
    


# --------- user registration api ---------
@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json

    current_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    f_name = data.get('f_name')
    l_name = data.get('l_name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    encripted_pass = generate_password_hash(password)

    created_at = data.get('created_at')

    # db-collection
    collection = db[user_collection_name]

    # duplication check
    existing_email = collection.find_one({'email': email})
    existing_phone = collection.find_one({'phone': phone})

    if validate_email_address(email) != 'True':
        return jsonify({'err': validate_email_address(email)})

    elif len(phone) > 10 or len(phone) < 10:
        return jsonify({'err': 'Enter correct phone no'})

    elif validate_password(password) != "True":
        return jsonify({'err': validate_password(password)})

    elif existing_email:
        return jsonify({'err': "existing email"})

    elif existing_phone:
        return jsonify({'err': "existing phone"})

    #  ----------- final api hit ---------------
    else:
        user = {'f_name': f_name,
                'l_name': l_name,
                'email': email,
                'phone': phone,
                'password': encripted_pass,
                'created_at': current_dt}

        result = collection.insert_one(user)

        return jsonify({'message': 'Welcome Onboard !'})




if __name__ == '__main__':
    app.run(port=5001, debug=True)
