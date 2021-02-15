from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired


class MonitorData(FlaskForm):
    lowBloodPressure = FloatField('Diastolic (bottom) Blood Pressure', validators=[DataRequired()])
    highBloodPressure = FloatField('Systolic (top) Blood Pressure', validators=[DataRequired()])
    bloodSugar = FloatField('Blood Sugar', validators=[DataRequired()])
    submit = SubmitField('Submit')
