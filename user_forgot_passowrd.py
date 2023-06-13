from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_mail import Mail, Message



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


# Email config 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'animeshbanerjeeshbl@gmail.com'
# app.config['MAIL_PASSWORD'] = '@Nimeshece1998'

mail = Mail(app)


@app.route('/api/v1/forgotpassword' , methods=['POST'])
def forgotpassword():
    data = request.json
    
    user_email = data.get('email')
    
    # Retrieve the user from the database based on the email
    user_data = collection.find_one({'email': user_email})
    
    current_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if user_data is None:
        return jsonify({"message": f"We can't find you with - {user_email}"})
    
    else:
        user_email_from_db =  user_data['email']
        user_password_from_db =  user_data['password']
        
        # decrypted_password = cipher_suite.decrypt(user_password_from_db.encode()).decode()

        
        # Send the decrypted password to the user's email
        message = Message('Decrypted Password', sender=app.config['MAIL_USERNAME'], recipients=[user_email_from_db])
        message.body = "Your decrypted password is: {decrypted_password}"
        mail.send(message)
        
        return jsonify({"message": f"Password has been sent to your registered email-id ({user_email})"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)