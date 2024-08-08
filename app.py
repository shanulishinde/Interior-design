from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate



app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'dfhdffjeryrjbvnuluite'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    number = data.get('number')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check for missing username
    if not username:
        return jsonify({'message': 'Username is required'}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, number=number, username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(email=username).first()  # Assume login with email
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify({'token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/')
def startlogin():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/hall')
def hall():
    return render_template('hall.html')

@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/backyard')
def backyard():
    return render_template('backyard.html')

@app.route('/dinning')
def dinning():
    return render_template('dining.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to list all users in JSON format
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_list = [{'id': user.id,'name':user.name,'username': user.username, 'number':user.number,'email': user.email} for user in users]
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
