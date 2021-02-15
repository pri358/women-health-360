import datetime
from women360 import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    fitnessData = db.relationship('FitnessData', backref='user')
    menstruationData = db.relationship('MenstruationData', backref='user')
    predictions = db.relationship('Predictions', backref='user')
    healthData = db.relationship('HealthData', backref='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class FitnessData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    age = db.Column(db.Integer, default = None)
    height = db.Column(db.Float, default = None)
    weight = db.Column(db.Float, default = None)
    avgPeriodLen = db.Column(db.Integer, default = None)
    avgCycleLen = db.Column(db.Integer, default = None)
    lastPeriodStart = db.Column(db.Date(), default = None)
    lastPeriodEnd = db.Column(db.Date(), default = None)

    def __init__(self, user_id, age, height, weight, avgPeriodLen, avgCycleLen, lastPeriodStart, lastPeriodEnd):
        self.user_id = user_id
        self.age = age
        self.avgPeriodLen = avgPeriodLen
        self.avgCycleLen = avgCycleLen
        self.lastPeriodStart = lastPeriodStart
        self.lastPeriodEnd = lastPeriodEnd
        self.height = height
        self.weight = weight

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return str(self.user_id)

    def get_user(self):
        return User.query.get(self.user_id)

    def updateLastPeriod(self, startDate, endDate):
        self.lastPeriodStart = startDate
        self.lastPeriodEnd = endDate


class MenstruationData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    startDate = db.Column(db.Date(), default = None)
    endDate = db.Column(db.Date(), default = None)
    comment = db.Column(db.String(250), default=None)

    def __init__(self, user_id, startDate, endDate, comment):
        self.user_id = user_id
        self.startDate = startDate
        self.endDate = endDate
        self.comment = comment


class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nextPeriodStart = db.Column(db.Date())
    nextPeriodEnd = db.Column(db.Date())

    def __init__(self, user_id):
        self.user_id = user_id

    def updateNextPeriod(self, periodEntries, periodData):
        self.nextPeriodStart, self.nextPeriodEnd = self.predict(periodEntries, periodData)

    def predict(self, periodEntries, periodData):
        if periodData.avgCycleLen and periodData.avgPeriodLen:
            nextStartDate = periodData.lastPeriodStart + datetime.timedelta(periodData.avgCycleLen)
            nextEndDate = nextStartDate + datetime.timedelta(periodData.avgPeriodLen)
            return nextStartDate, nextEndDate
        return None, None


class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    lowBloodPressure = db.Column(db.Float)
    highBloodPressure = db.Column(db.Float)
    bloodSugar = db.Column(db.Float)

    def __init__(self, user_id, lowBloodPressure, highBloodPressure, bloodSugar):
        self.user_id = user_id
        self.bloodSugar = bloodSugar
        self.lowBloodPressure = lowBloodPressure
        self.highBloodPressure = highBloodPressure
