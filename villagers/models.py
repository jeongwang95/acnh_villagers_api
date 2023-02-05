from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    villager = db.relationship('Villager', backref = 'owner', lazy = True)

    def __init__(self, email, password, first_name, last_name, id = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)
        
    def __repr__(self):
        return f"User {self.email} has been added to the databse!"

class Villager(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    species = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    birthday = db.Column(db.String(50))
    personality = db.Column(db.String(50))
    hobby = db.Column(db.String(50))
    phrase = db.Column(db.String(50))
    image = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, name, species, gender, birthday, personality, hobby, phrase, image, user_id, id=''):
        self.id = self.set_id()
        self.name = name
        self.species = species
        self.gender = gender
        self.birthday = birthday
        self.personality = personality
        self.hobby = hobby
        self.phrase = phrase
        self.image = image
        self.user_id = user_id

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"{self.name} has been added to your village!"

class VillagerSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'species', 'gender', 'birthday', 'personality', 'hobby', 'phrase', 'image']

villager_schema = VillagerSchema()
villagers_schema = VillagerSchema(many=True)
