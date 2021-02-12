# Women Health and Fitness 360 App
## A fitness app designed specifically to cater women 

This app is divided into 3 major components:
1. Menstruation Cycles 
2. Health Monitor 
3. Nutrition and Exercise 

**1. Menstruation Cycles:**
The main features are:
  1. Recording and Predicting: Predicting the next cycle bbased on the recorded data. AI and ML techniques can be used for this. For the proof of concept, a simple technique using average period length is applied in the protoype.
  2. Myths and FAQs
  3. Discussion Forum: A private forum where users can discuss their problems.
  
**2. Health Monitor:**
The main features are:
  1. Monitor Regular Data: Regular data like number of steps, heart rate, sleep hours, etc which can be leveraged from other apps.
  2. Monitor Additional Health Data: Since this app tries to include women of all ages, regular health data like blood pressure, blood glucose can also be monitored.
  3. Irregularity Detection: Detect in case there is an anomaly in the health data. 
  For irregularity detection, currently the history and the data from patients with same age is taken, and some limits are set on the basis of standard deviation. 
  More advanced ML techniques like outlier detection can also be used for the same. 
  
 **3. Nutrition and Fitness:**
The main features are:
  1. Reciped Ideas
  2. Different Exercise Routines
  3. Personalised Exercise and Workout Routines
 
 Some Challenges and future add-ons: 
 1. For gender verification, some steps can be applied like using a 3rd party government authentication and  real-time verification using image processing
 2. For monitoring health data, data from other health apps can be leveraged. 
 3. In the discussion forum, permission will be required to reveal the identity of the user. If denied, anonymity will be maintained. 
 4. While detecting anomalities in the health data, data from similar users (similar age, weight and height) can be used. 
 5. To increase privacy of the app, two-factor authentication can be used.

**Please Note that this is a function prototype and all of the features aren't yet implemented.**

To run the app, please run the file **run.py**

Dummy-data is used in the database. 

Login credentials: email - test@gmail.com password - test

 Please find the screen recording of the app: screen.mp4


