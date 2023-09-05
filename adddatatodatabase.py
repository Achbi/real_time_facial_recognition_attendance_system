import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


#cred = credentials.Certificate('your_config.json')
#firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-firebase-db'})




cred = credentials.Certificate('faceattendancerealtime-ec57d-firebase-adminsdk-2ldm3-a0d454d74a.json')
firebase_admin = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancerealtime-ec57d-default-rtdb.firebaseio.com'
})

ref = db.reference('Students')

data ={# nested  dictionary
    "2201140":
        {
            "name": "Raghav Bahety",
            "major": "MBA",
            "starting_year" :2022,
            "Total attendance" :6,
            "standing": "O",
            "Year":2,
            "last_attendacne_time":"2023-08-20 12:43:20"

         },

    "2201141":
        {
            "name": "HIMANSHU KUMAR",
            "major": "BTECH",
            "starting_year": 2022,
            "Total attendance": 6,
            "standing": "CSE",
            "Year": 2,
            "last_attendacne_time": "2023-08-20 12:43:20"
        },
    "2201142":
    {
      "name": "harshit bahety",
      "major":"ECE",
      "starting year":2022,
      "Total attendance":6,
      "standing":"0",
      "year":2,
      "last_attendacne_time": "2023-08-20 12:43:20"

    },

}
for key,value in data.items():
    ref.child(key).set(value)
