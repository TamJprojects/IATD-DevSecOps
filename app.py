import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Decide if you want to serve a vulnerable version or not!
# DO NOTE: some functionalities will still be vulnerable even if the value is
# set, as it is a matter of bad practice. Such an example is the debug mode.

vuln = int(os.getenv('vulnerable', 1))
# token alive for how many seconds?
alive = int(os.getenv('tokentimetolive', 60))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/get_user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    
    if vuln:
        # Vulnerable SQL query
        query = f"SELECT * FROM user WHERE username = '{username}'"
        user = db.session.execute(query).fetchone()
    else:
        # Secure SQL query
        user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify({"id": user.id, "username": user.username, "email": user.email})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
