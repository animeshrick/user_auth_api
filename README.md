# user_auth_api

# Register API :
### URL : http://127.0.0.1:2023/api/v1/register
### Method: POST
### Params (Body): f_name : Test | l_name : test | email : test@gmail.com | phone : 1231231231 | password : @A123456
### Key Features: Password encription | Email & Phone Validation | Password Validation | Existing Eemail & Phone no

# Login API :
### URL : http://127.0.0.1:2023/api/v1/login
### Method: POST
### Params (Body): email_phone : test@gmail.com | password : @A123456
### Key Features: Password checking | Email & Phone is Valid | Password Validation | Existing Eemail & Phone no

# Reset Password API :
### URL : http://127.0.0.1:2023/api/v1/resetpassword
### Method: POST
### Params (Body): user_id : {get from DB} | new_pass : @A123456 | conf_pass : @A123456
### Key Features: Password checking | Update old password with new password | Password Validation

# View All User API :
### URL : http://127.0.0.1:2023/api/v1/users
### Method: GET
### Params (Body): NONE
### Key Features: For Admin use only
