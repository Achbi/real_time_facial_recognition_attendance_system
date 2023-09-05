import bbox as bbox
import cv2
import os
import pickle
import numpy
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate('faceattendancerealtime-ec57d-firebase-adminsdk-2ldm3-a0d454d74a.json')
firebase_admin = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancerealtime-ec57d-default-rtdb.firebaseio.com',
    'storageBucket': 'faceattendancerealtime-ec57d.appspot.com'


})

bucket = storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imgBackground = cv2.imread('resources/background.png')

foldermodepath = 'resources/modes'
modepathList = os.listdir(foldermodepath)
imgModeList = []


for path in modepathList:
   imgModeList.append(cv2.imread(os.path.join(foldermodepath, path)))
print(len(imgModeList))
#load the encoding file
file = open('encodefile.p','rb')
encodelistknownwithid = pickle.load(file)
file.close()
encodelistknown, studentIds = encodelistknownwithid
print(studentIds)

modeType = 0
counter = 0
id = 0
imgstudent = []



while True:
   Success, img = cap.read()

   imgs= cv2.resize(img, (0 , 0), None, 0.25, 0.25)
   imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

   facecurframe = face_recognition.face_locations(imgs)
   encodecurframe = face_recognition.face_encodings(imgs, facecurframe)
   imgBackground[162:162 + 480, 55:55 + 640] = img
   imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

   if facecurframe:

    for encodeface, faceloc in zip(encodecurframe,facecurframe):
       #zip method is to use two loops together


       matches = face_recognition.compare_faces(encodelistknown,encodeface)

       facedis = face_recognition.face_distance(encodelistknown,encodeface) #lower the face dis value better it is


       matchindex = np.argmin(facedis)
       #print(matchindex)
       if matches[matchindex]:
        print("known face detected")
        y1, x2, y2, x1 = faceloc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

        id =studentIds[matchindex]
        if counter ==0:
           # cvzone.putTextRect(imgBackground, "Loading", (276, 400))
            text_color = (0, 255, 0)
          #  cvzone.putTextRect(imgBackground, "Loading", (276, 400))
            cv2.imshow("FACE ATTENDANCE", imgBackground)
            cv2.waitKey(1)
            counter =1
            modeType =1




    if counter != 0 :
        if counter == 1:

            studentsInfo = db.reference(f'Students/{id}').get()
            print(studentsInfo)
            blob = bucket.get_blob(f'IM/{id}.jpg')

            array = np.frombuffer(blob.download_as_string(), np.uint8)

            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            #update the attendance
            datetimeObject = datetime.strptime(studentsInfo['last_attendacne_time'],"%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            print("date time now",datetime.now())
            print("date time object -last attendance time ",datetimeObject)
            print(secondsElapsed)
            if secondsElapsed > 30:



                 ref =db.reference(f'Students/{id}')

                 studentsInfo['Total attendance'] +=1
                 ref.child('Total attendance').set(studentsInfo['Total attendance'])
                 ref.child('last_attendacne_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                 print(secondsElapsed)
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                print(modeType)

        if modeType != 3:



            if 10<counter<20:
             modeType = 2

            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if counter<=10:

                cv2.putText(imgModeList[1],str(studentsInfo['Total attendance']),(60,80),
                cv2.FONT_HERSHEY_COMPLEX,1,(225,225,255),1)


                cv2.putText(imgModeList[1], str(studentsInfo['major']), (193, 507),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (225, 225, 255), 1)


                cv2.putText(imgModeList[1], str(id), (193, 450),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (225,225, 255), 1)


                cv2.putText(imgModeList[1], str(studentsInfo['standing']), (107, 583),
          cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                cv2.putText(imgModeList[1], str(studentsInfo['Year']), (214, 583),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                cv2.putText(imgModeList[1], str(studentsInfo['starting_year']), (333, 583),
                  cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgModeList[1], str(studentsInfo['name']), (122, 401),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                imgModeList[1][127:127 + 216, 103:103 + 216] = imgStudent

    counter += 1

    if counter >= 20:
      counter = 0
      modeType = 0
      studentInfo = []
      imgStudent = []
      imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
   else:
    modeType = 0
    counter = 0
    # cv2.imshow("Webcam", img)
    #cv2.imshow("Face Attendance", imgBackground)
    #cv2.waitKey(1)
    imgBackground[162:162+480, 55:55 +640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
   cv2.imshow("FACE ATTENDANCE", imgBackground)
   cv2.waitKey(1)


