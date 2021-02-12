from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired


class MonitorData(FlaskForm):
    lowBloodPressure = FloatField('Low Blood Pressure', validators=[DataRequired()])
    highBloodPressure = FloatField('High Blood Pressure', validators=[DataRequired()])
    bloodSugar = FloatField('Blood Sugar', validators=[DataRequired()])
    submit = SubmitField('Submit')
