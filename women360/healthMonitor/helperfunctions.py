import numpy as np
from sqlalchemy import desc

from women360.models import FitnessData, HealthData


def detectAnomaly(data, curValue):
    data = np.array(data)
    dataStd = np.std(data)
    dataMean = np.mean(data)
    cutOff = dataStd
    lowerLimit = dataMean - cutOff
    upperLimit = dataMean + cutOff
    if curValue > upperLimit:
        return "high"
    if curValue < lowerLimit:
        return "low"
    return "normal"

def detectManually(curValue, lowLimit, highLimit):
    if curValue < lowLimit:
        return "low"
    elif curValue > highLimit: 
        return "high"
    return "normal"


def checkBloodPressure(user_id):
    user = HealthData.query.filter_by(user_id=user_id).order_by(desc('timestamp')).limit(
        1).first()
    latestLowBloodPressure = user.lowBloodPressure
    latestHighBloodPressure = user.highBloodPressure

    dataLowBloodPressure = []
    dataHighBloodPressure = []
    pastData = HealthData.query.filter_by(user_id=user_id).all()
    for data in pastData:
        dataLowBloodPressure.append(data.lowBloodPressure)
        dataHighBloodPressure.append(data.highBloodPressure)
    user = FitnessData.query.filter_by(user_id=user_id).first()
    userAge = user.age
    relatedUsers = FitnessData.query.filter_by(age=userAge)
    for user in relatedUsers:
        relatedUserId = user.user_id
        relatedData = HealthData.query.filter_by(user_id=relatedUserId)
        for data in relatedData:
            dataLowBloodPressure.append(data.lowBloodPressure)
            dataHighBloodPressure.append(data.highBloodPressure)

    if len(dataLowBloodPressure) < 5:
        low = detectManually(latestLowBloodPressure, 60, 90)
        high = detectManually(latestHighBloodPressure, 80, 1202)
        
    else:
        low = detectAnomaly(dataLowBloodPressure, latestLowBloodPressure)
        high = detectAnomaly(dataHighBloodPressure, latestHighBloodPressure)

    if low == "high" or high == "high":
        return "high"
    if low == "low" or high == "low":
        return "low"
    return "normal"


def checkBloodSugar(user_id):
    user = HealthData.query.filter_by(user_id=user_id).order_by(desc('timestamp')).limit(
        1).first()
    if user is None:
        return None
    latestBloodSugar = HealthData.query.filter_by(user_id=user_id).order_by(desc('timestamp')).limit(
        1).first().bloodSugar

    dataBloodSugar = []
    pastData = HealthData.query.filter_by(user_id=user_id).all()
    for data in pastData:
        dataBloodSugar.append(data.bloodSugar)
    user = FitnessData.query.filter_by(user_id=user_id).first()
    userAge = user.age
    relatedUsers = FitnessData.query.filter_by(age=userAge)
    for user in relatedUsers:
        relatedUserId = user.user_id
        relatedData = HealthData.query.filter_by(user_id=relatedUserId)
        for data in relatedData:
            dataBloodSugar.append(data.bloodSugar)
    if len(dataBloodSugar) < 5:
        return detectManually(latestBloodSugar, 70, 140)
    return detectAnomaly(dataBloodSugar, latestBloodSugar)
