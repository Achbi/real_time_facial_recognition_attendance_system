import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate('faceattendancerealtime-ec57d-firebase-adminsdk-2ldm3-a0d454d74a.json')
firebase_admin = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancerealtime-ec57d-default-rtdb.firebaseio.com',
    'storageBucket': 'faceattendancerealtime-ec57d.appspot.com'


})


folderPath = 'IM'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
print(pathList)
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])


    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        print(encode)
        encodeList.append(encode)

    return encodeList
print("encoding started")

encodelistknown = findEncodings(imgList)
print(encodelistknown)
encodelistknownwithid = [encodelistknown,studentIds]
print("encoding done")


file = open('encodefile.p','wb')
pickle.dump(encodelistknownwithid,file)
file.close()
print("file saved")


