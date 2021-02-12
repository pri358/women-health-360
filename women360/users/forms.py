from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import DateField
from women360.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])
    height = FloatField('Height (in cms)', validators=[DataRequired()])
    weight = FloatField('Weight (in kgs)', validators=[DataRequired()])
    avgPeriodLen = IntegerField('Average Period Length', validators=[DataRequired(), NumberRange(1, 15, "Inapropriate "
                                                                                                        "Period "
                                                                                                        "Length")])
    avgCycleLen = IntegerField('Average Cycle Length', validators=[DataRequired()])
    lastPeriodStart = DateField('Last Period Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    lastPeriodEnd = DateField('Last Period End Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DataForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    height = FloatField('Height (in cms)', validators=[DataRequired()])
    weight = FloatField('Weight (in kgs)', validators=[DataRequired()])
    avgPeriodLen = IntegerField('Average Period Length', validators=[DataRequired(), NumberRange(1, 15, "Inappropriate "
                                                                                                        "Period "
                                                                                                        "Length")])
    avgCycleLen = IntegerField('Average Cycle Length', validators=[DataRequired()])
    lastPeriodStart = DateField('Last Period Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    lastPeriodEnd = DateField('Last Period End Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Update')
