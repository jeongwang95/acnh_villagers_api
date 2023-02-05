from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import VillagerForm
from ..models import Villager, db
from ..helpers import Villager_Data, acnh_data


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/', methods = ['GET', 'POST'])
@login_required
def profile():
    my_villager = VillagerForm()
    try:
        if request.method == "POST" and my_villager.validate_on_submit():

            # instantiate Villager_Data obj to look for the villager to get his/her info
            data = Villager_Data(my_villager.name.data.title().strip(), my_villager.species.data.title().strip())
            found = data.fill_info()

            if found:
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

    user_id = current_user.id

    villagers = Villager.query.filter_by(user_id = user_id).all()

    return render_template('profile.html', form=my_villager, villagers=villagers, count=len(villagers))

@site.route('/browse', methods = ['GET', 'POST'])
@login_required
def browse():
    return render_template('browse.html', species=acnh_data)