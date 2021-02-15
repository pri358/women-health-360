from flask import render_template, url_for, flash, redirect, request, Blueprint, escape
from flask_login import login_user, current_user, logout_user, login_required
from women360 import db, bcrypt
from women360.models import User, FitnessData, Predictions
from women360.users.forms import (RegistrationForm, LoginForm, DataForm)
from datetime import datetime, date

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f"Hey {current_user.username}", "info")
        return redirect(url_for('home.homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You have been logged in', 'success')
        return redirect(url_for('users.profile'))
    return render_template('register.html', title='Register and Info', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f"Hey {current_user.username}", "info")
        return redirect(url_for('home.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('home.homepage'))


@users.route("/profile", methods = ['GET', 'POST'])
@login_required
def profile():
    form = DataForm()
    if request.method == 'POST' and form.validate_on_submit():
        date_format = "%Y-%m-%d"
        # dob = datetime.strptime(escape(form.dob.data), date_format)
        startDate = datetime.strptime(escape(form.lastPeriodStart.data), date_format)
        endDate = datetime.strptime(escape(form.lastPeriodEnd.data), date_format)
        # age = date.today().year - dob.year
        age  = form.age.data
        fitnessData = FitnessData(current_user.id, age, form.height.data, form.weight.data, form.avgPeriodLen.data, form.avgCycleLen.data,
                                  startDate, endDate)
        predictions = Predictions(user_id=current_user.id)
        predictions.updateNextPeriod([], fitnessData)
        db.session.add(predictions)
        db.session.add(fitnessData)
        db.session.commit()
        flash('Information successfully updated!')
        return redirect(url_for('home.homepage'))
    return render_template('updateInfo.html', title='Update Profile', form=form, name = current_user.username, email = current_user.email, update = True)




@users.route("/update", methods=['GET', 'POST'])
@login_required
def update():
    fitnessData = FitnessData.query.filter_by(user_id=current_user.id).first()
    form = DataForm()

    if request.method == 'POST' and form.validate_on_submit():
        date_format = "%Y-%m-%d"
        startDate = datetime.strptime(escape(form.lastPeriodStart.data), date_format)
        endDate = datetime.strptime(escape(form.lastPeriodEnd.data), date_format)
        fitnessData.age = form.age.data
        fitnessData.height = form.height.data
        fitnessData.weight = form.weight.data
        fitnessData.avgCycleLen = form.avgCycleLen.data
        fitnessData.avgPeriodLen = form.avgPeriodLen.data
        fitnessData.lastPeriodStart = startDate
        fitnessData.lastPeriodEnd = endDate
        predictions = Predictions.query.filter_by(user_id=current_user.id).first()
        predictions.updateNextPeriod([], fitnessData)
        db.session.commit()
        flash('Information successfully updated!')
        return redirect(url_for('home.homepage'))

    elif request.method == 'GET' and fitnessData:
        form.age.data = fitnessData.age
        form.height.data = fitnessData.height
        form.weight.data = fitnessData.weight
        form.avgCycleLen.data = fitnessData.avgCycleLen
        form.avgPeriodLen.data = fitnessData.avgPeriodLen
        form.lastPeriodStart.data = fitnessData.lastPeriodStart
        form.lastPeriodEnd.data = fitnessData.lastPeriodEnd

    return render_template('updateInfo.html', title='Update Profile', form=form, name = current_user.username, email = current_user.email, update = False)
