from flask import render_template, url_for, flash, redirect, request, Blueprint, escape
from flask_login import  current_user, login_required
from women360 import db
from women360.models import FitnessData, MenstruationData, Predictions
from women360.menstruation.forms import RecordData
from datetime import datetime

menstruation = Blueprint('menstruation', __name__)


@menstruation.route("/periods/home", methods=['GET', 'POST'])
@login_required
def periods():
    fitnessData = FitnessData.query.filter_by(user_id=current_user.id).first()
    predictions = Predictions.query.filter_by(user_id=current_user.id).first()
    return render_template('periodHome.html', data=fitnessData, predictions=predictions)


@menstruation.route("/periods/track", methods=['GET', 'POST'])
@login_required
def track():
    form = RecordData()
    if request.method == 'POST' and form.validate_on_submit():
        date_format = "%Y-%m-%d"
        startDate = datetime.strptime(escape(form.startDate.data), date_format)
        endDate = datetime.strptime(escape(form.endDate.data), date_format)
        comment = escape(form.comment.data)
        data = MenstruationData(current_user.id, startDate, endDate, comment)
        fitnessData = FitnessData.query.filter_by(user_id=current_user.id).first()
        fitnessData.updateLastPeriod(startDate, endDate)
        predictions = Predictions.query.filter_by(user_id=current_user.id).first()
        predictions.updateNextPeriod([], fitnessData)
        db.session.add(data)
        db.session.commit()
        flash('Period Info Added')
        return redirect(url_for('menstruation.periods'))
    return render_template('trackPeriods.html', title='Track Periods', form=form)
