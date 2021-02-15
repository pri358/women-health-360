from flask import render_template, url_for, flash, redirect, request, Blueprint, escape
from flask_login import login_user, current_user, logout_user, login_required
from women360 import db, bcrypt
from women360.models import User, FitnessData, MenstruationData, Predictions, HealthData
from women360.healthMonitor.forms import MonitorData
from women360.healthMonitor.helperfunctions import checkBloodPressure, checkBloodSugar
from sqlalchemy import desc

healthMonitor = Blueprint('healthMonitor', __name__)


@healthMonitor.route("/health/home", methods=['GET', 'POST'])
@login_required
def healthHome():
    fitnessData = FitnessData.query.filter_by(user_id=current_user.id).first()
    healthData = HealthData.query.filter_by(user_id=current_user.id).order_by(desc('timestamp')).limit(
        1).first()
    val = None
    sugar = None
    if fitnessData and healthData:
        val = checkBloodPressure(current_user.id)
        sugar = checkBloodSugar(current_user.id)
    return render_template('healthHome.html', bp=val, sugar=sugar, fitnessData = fitnessData, healthData = healthData)


@healthMonitor.route("/health/monitor", methods=['GET', 'POST'])
@login_required
def monitor():
    form = MonitorData()
    if request.method == 'POST' and form.validate_on_submit():
        data = HealthData(current_user.id, form.lowBloodPressure.data, form.highBloodPressure.data, form.bloodSugar.data)
        db.session.add(data)
        db.session.commit()
        flash('Health Data Added', 'success')
        return redirect(url_for('healthMonitor.healthHome'))
    return render_template('monitorData.html', title='Add Today\'s Data', form=form)
