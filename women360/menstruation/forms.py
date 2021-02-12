from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import DateField


class RecordData(FlaskForm):
    startDate = DateField('Period Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    endDate = DateField('Period End Date', validators=[DataRequired()], format='%Y-%m-%d')
    comment = StringField('Additional Comments')
    submit = SubmitField('Submit')
