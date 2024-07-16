from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('You have Signed In successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('auth.sign_in'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be more than 4 characters.", category='error')
        elif password1 != password2:
            flash("Passwords do not match.", category='error')
        elif len(password1) < 7:
            flash("Password must be more than 7 characters.", category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account has been created!", category='success')
            return redirect(url_for('routes.home'))

    return render_template('registration.html', user=current_user)