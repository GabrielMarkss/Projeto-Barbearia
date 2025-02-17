from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
from jose import jwt
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = '62999727983'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gabriel@localhost:5432/db_barber'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
CORS(app)  # Ativar CORS para permitir comunicação com o frontend Angular

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Campos obrigatórios.'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'E-mail ou senha inválidos!'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.component.html')

if __name__ == '__main__':
    app.run(debug=True)
