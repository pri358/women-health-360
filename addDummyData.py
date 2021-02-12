from women360.models import User, FitnessData, Predictions, HealthData
from women360 import db, bcrypt
from datetime import date
import pandas as pd
import random

df = pd.read_csv('mock-data.csv')
names = df["username"]
emails = df["email"]
passwords = df["password"]
ages = list(range(20, 45, 1))
heights = list(range(150, 180, 4))
weights = list(range(50, 80, 2))
periodLengths = list(range(3, 7, 1))
cycleLengths = list(range(25, 31, 1))
startDates = [date(2020, 2, 1), date(2020, 2, 2), date(2020, 2, 3)]
endDates = [date(2020, 2, 5), date(2020, 2, 7), date(2020, 2, 10)]
lowBPs = list(range(70, 90, 1))
highBPs = list(range(110, 130, 1))
sugars = list(range(120, 140, 4))


def addUser(name, email, password):
    user = User(name, email, bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    return user.id


def addFitness(user_id, age, height, weight, periodLen, cycleLen, startDate, endDate):
    fitness = FitnessData(user_id, age, height, weight, periodLen, cycleLen, startDate, endDate)
    predictions = Predictions(user_id)
    predictions.updateNextPeriod([], fitness)
    db.session.add(predictions)
    db.session.add(fitness)
    db.session.commit()


def addHealth(user_id, lowBP, highBP, sugar):
    health1 = HealthData(user_id, lowBP, highBP, sugar)
    health2 = HealthData(user_id, lowBP + 2, highBP - 2, sugar + 1)
    for i in range(5):
        db.session.add(health1)
        db.session.add(health2)
    db.session.commit()


def addData():
    for i in range(100):
        user_id = addUser(names[i], emails[i], passwords[i])
        addFitness(user_id, random.choice(ages), random.choice(heights), random.choice(weights),
                   random.choice(periodLengths), random.choice(cycleLengths),
                   random.choice(startDates), random.choice(endDates))
        addHealth(user_id, random.choice(lowBPs), random.choice(highBPs), random.choice(sugars))
