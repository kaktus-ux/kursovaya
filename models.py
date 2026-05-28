from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # Храните пароли в хэшированном виде
    role = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    contact_info = db.Column(db.String(200), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200), nullable=False)
  