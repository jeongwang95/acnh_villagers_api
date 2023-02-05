from flask import Blueprint, render_template, request, redirect, url_for, flash
from villagers.forms import UserSigninForm, UserSignupForm
from villagers.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email = email).all()
            if not user:
                first_name = form.first_name.data
                last_name = form.last_name.data
                password = form.password.data

                user = User(email, password, first_name.title().strip(), last_name.title().strip())

                db.session.add(user)
                db.session.commit()

                flash(f"{first_name.title().strip()}, you have succesfully created your account!", "user-created")

                return redirect(url_for('auth.signin'))
            else:
                flash(f"An account with the email: {email} already exists!", "email-exists")

                return redirect(url_for('auth.signup'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signup.html', form=form)
    
@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Login Successful!', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                print("auth-fail")
                flash('Email or Password was incorrect! Double check your information and try again.', 'auth-fail')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))
