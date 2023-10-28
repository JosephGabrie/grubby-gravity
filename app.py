from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Josephg57!@database-1.cli2y73ygj8q.us-east-1.rds.amazonaws.com/FriendDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#adding CORS (Cross-Origin Resource Sharing) because I am using both astro and flask
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api/users')
def api_users():
    users = User.query.all()
    return jsonify([{'username': user.username, 'email': user.email} for user in users])

@app.route('/add_user/<username>/<email>')
def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return f"User {username} added to database"

