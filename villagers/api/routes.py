from flask import Blueprint, request, jsonify
from villagers.helpers import token_required, Villager_Data
from villagers.models import db, Villager, villager_schema, villagers_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# Create villager endpoint
@api.route('/villagers', methods = ['POST'])
@token_required
def create_villager(our_user):
    name = request.json['name'].title().strip()
    species = request.json['species'].title().strip()
    user_id = our_user.id

    data = Villager_Data(name, species)
    found = data.fill_info()

    if found:
        if Villager.query.filter_by(name=name, user_id=user_id).first():
            return jsonify({'message': 'Cannnot add duplicates in one account.'}), 401
        else:
            gender = data.gender
            birthday = data.birthday
            personality = data.personality
            hobby = data.hobby
            phrase = data.phrase
            image = data.image

            villager = Villager(name, species, gender, birthday, personality, hobby, phrase, image, user_id)

            db.session.add(villager)
            db.session.commit()

            response = villager_schema.dump(villager)

            return jsonify(response)
    else:
        return jsonify({'message': 'Valid name and species required!'}), 401

# Retrieve all villagers endpoint
@api.route('/villagers', methods = ['GET'])
@token_required
def get_villagers(our_user):
    owner = our_user.id
    villagers = Villager.query.filter_by(user_id = owner).all()
    response = villagers_schema.dump(villagers)

    return jsonify(response)

# Retrieve one villager endpoint
@api.route('/villagers/<id>', methods = ['GET'])
@token_required
def get_villager(our_user, id):
    owner = our_user.id
    if owner == our_user.id:
        villager = Villager.query.get(id)
        response = villager_schema.dump(villager)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401

# Update villager endpoint
@api.route('/villagers/<id>', methods = ['PUT','POST'])
@token_required
def update_villager(our_user, id):
    villager = Villager.query.get(id)
    villager.name = request.json['name'].title().strip()
    villager.species = request.json['species'].title().strip()
    villager.user_id = our_user.id

    data = Villager_Data(villager.name, villager.species)
    found = data.fill_info()

    if found:
        villager.gender = data.gender
        villager.birthday = data.birthday
        villager.personality = data.personality
        villager.hobby = data.hobby
        villager.phrase = data.phrase
        villager.image = data.image

        db.session.commit()
        response = villager_schema.dump(villager)
        return jsonify(response)

    else:
        return jsonify({'message': 'Valid name and species required!'}), 401

# Delete villager endpoint
@api.route('/villagers/<id>', methods = ['DELETE'])
@token_required
def delete_villager(our_user, id):
    villager = Villager.query.get(id)
    db.session.delete(villager)
    db.session.commit()

    response = villager_schema.dump(villager)
    return jsonify(response)