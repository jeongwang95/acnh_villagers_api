from functools import wraps
import secrets
from flask import request, jsonify, json, flash, redirect, url_for
import requests
from villagers.models import User
import decimal

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(id=token).first()
            print(our_user)
            if not our_user or our_user.id != token:
                return jsonify({'message': 'Token is invalid'})

        except:
            owner = User.query.filter_by(id=token).first()
            if token != owner.id and secrets.compare_digest(token, owner.id):
                return jsonify({'message': 'Token is invalid'})
        
        return our_flask_function(our_user, *args, **kwargs)
    
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# make an api request to ACNH API (3rd party API) to get the json file that has all villager info
def get_all_villager_info():
    r = requests.get('https://acnhapi.com/v1/villagers/')

    if r.status_code == 200:
        data = r.json()
        
        keys = ['Alligator', 'Anteater', 'Bear', 'Bird', 'Bull', 'Cat', 'Chicken', 'Cow', 'Cub', 'Deer', 'Dog', 'Duck', 'Eagle', 'Elephant', 'Frog', 'Goat', 'Gorilla', 'Hamster', 'Hippo', 'Horse', 'Kangaroo', 'Koala', 'Lion', 'Monkey', 'Mouse', 'Octopus', 'Ostrich', 'Penguin', 'Pig', 'Rabbit', 'Rhino', 'Sheep', 'Squirrel', 'Tiger', 'Wolf']
        d = {key: [] for key in keys}
        
        # organize the json file by creating a new dictionary
        # key = species name, value = list of villagers who are those species
        for id, v in data.items():
            if 'crd' in id:
                d['Alligator'].append(v)
            elif 'ant' in id:
                d['Anteater'].append(v)
            elif 'bea' in id:
                d['Bear'].append(v)
            elif 'brd' in id:
                d['Bird'].append(v)
            elif 'bul' in id:
                d['Bull'].append(v)
            elif 'cat' in id:
                d['Cat'].append(v)
            elif 'chn' in id:
                d['Chicken'].append(v)
            elif 'cow' in id:
                d['Cow'].append(v)
            elif 'cbr' in id:
                d['Cub'].append(v)
            elif 'der' in id:
                d['Deer'].append(v)
            elif 'dog' in id:
                d['Dog'].append(v)
            elif 'duk' in id:
                d['Duck'].append(v)
            elif 'pbr' in id:
                d['Eagle'].append(v)
            elif 'elp' in id:
                d['Elephant'].append(v)
            elif 'flg' in id:
                d['Frog'].append(v)
            elif 'goa' in id:
                d['Goat'].append(v)
            elif 'gor' in id:
                d['Gorilla'].append(v)
            elif 'ham' in id:
                d['Hamster'].append(v)
            elif 'hip' in id:
                d['Hippo'].append(v)
            elif 'hrs' in id:
                d['Horse'].append(v)
            elif 'kgr' in id:
                d['Kangaroo'].append(v)
            elif 'kal' in id:
                d['Koala'].append(v)
            elif 'lon' in id:
                d['Lion'].append(v)
            elif 'mnk' in id:
                d['Monkey'].append(v)
            elif 'mus' in id:
                d['Mouse'].append(v)
            elif 'ocp' in id:
                d['Octopus'].append(v)
            elif 'ost' in id:
                d['Ostrich'].append(v)
            elif 'pgn' in id:
                d['Penguin'].append(v)
            elif 'pig' in id:
                d['Pig'].append(v)
            elif 'rbt' in id:
                d['Rabbit'].append(v)
            elif 'rhn' in id:
                d['Rhino'].append(v)
            elif 'shp' in id:
                d['Sheep'].append(v)
            elif 'squ' in id:
                d['Squirrel'].append(v)
            elif 'tig' in id:
                d['Tiger'].append(v)
            elif 'wol' in id:
                d['Wolf'].append(v)
        return d
    else:
        flash(f"Could not access ACNH API", "bad-request")
        return redirect(url_for('site.profile'))

# json file from ACNH API is stored into a global variable
acnh_data = get_all_villager_info()

# this class is used to get the data of a villager to instantiate our Villager class
class Villager_Data():

    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.gender = ''
        self.birthday = ''
        self.personality = ''
        self.hobby = ''
        self.phrase = ''
        self.image = ''

    def fill_info(self):
        found = False # flag used to let us know if the villager was in ACNH API
        
        # check if species is an Animal Crossing species
        if self.species not in acnh_data:
            return found

        # check if villager exists
        for villager in acnh_data[self.species]:
            if villager['name']['name-USen'] == self.name:
                self.gender = villager['gender']
                self.birthday = villager['birthday-string']
                self.personality = villager['personality']
                self.hobby = villager['hobby']
                self.phrase = villager['catch-phrase']
                self.image = villager['image_uri']
                found = True
                break
        return found
            


