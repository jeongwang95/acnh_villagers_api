from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import VillagerForm, RemoveForm
from ..models import Villager, db
from ..helpers import Villager_Data, acnh_data


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/', methods = ['GET', 'POST', 'DELETE'])
@login_required
def profile():
    my_villager = VillagerForm()
    remove_villager = RemoveForm()
    try:
        if request.method == "POST" and my_villager.validate_on_submit():

            # instantiate Villager_Data obj to look for the villager to get his/her info
            data = Villager_Data(my_villager.name.data.title().strip(), my_villager.species.data.title().strip())
            found = data.fill_info()

            if found:
                # check if the villager is already in user's collection
                if Villager.query.filter_by(name=data.name, user_id=current_user.id).first():
                    flash(f"{my_villager.name.data.title().strip()} is already in your collection!", 'repeat')
                    return redirect(url_for('site.profile'))
                else:
                    name = data.name
                    species = data.species
                    gender = data.gender
                    birthday = data.birthday
                    personality = data.personality
                    hobby = data.hobby
                    phrase = data.phrase
                    image = data.image
                    user_id = current_user.id

                    villager = Villager(name, species, gender, birthday, personality, hobby, phrase, image, user_id)

                    db.session.add(villager)
                    db.session.commit()
            else:
                flash(f"{my_villager.name.data.title().strip()} the {my_villager.species.data.title().strip()} could not be added to your collection. Please double check both NAME & SPECIES then try again.", 'fail-search')

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Could not add villager, please check your form and try again!")

    try:
        if request.method == 'DELETE' and remove_villager.validate_on_submit():
            remove = Villager.query.get(remove_villager.remove_name.title().strip())
            print('HELLO IM HERE!')
            if remove:
                db.session.delete(remove)
                db.session.commit()
            else:
                flash(f"Could not {remove_villager.remove_name.data.title().strip()}. Double check your spelling then try again.", 'fail-remove')
            
            return redirect(url_for('site.profile'))

    except:
        raise Exception("Could not remove villager, please check your form and try again!")

    user_id = current_user.id

    villagers = Villager.query.filter_by(user_id = user_id).all()

    return render_template('profile.html', form=my_villager, villagers=villagers, count=len(villagers), remove=remove_villager)

@site.route('/browse', methods = ['GET', 'POST'])
@login_required
def browse():
    return render_template('browse.html', species=acnh_data)