import os
import cv2
import face_recognition
import mysql.connector

dbCon = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="firstdemo"
)
conn = dbCon.cursor()

party_photos_dir = "/Users/karthi/Photos/sports-day-photos"
party_photos = os.listdir(party_photos_dir)

# Loop through all photos and compare faces to the reference selfie image
for photo in party_photos:
    photo_path = os.path.join(party_photos_dir, photo)
    photo_image = cv2.imread(photo_path)
    photo_image = cv2.cvtColor(photo_image, cv2.COLOR_BGR2RGB)
    photo_encodings = face_recognition.face_encodings(photo_image)
    if len(photo_encodings) > 0:
        for encoding in photo_encodings:
            conn.execute("INSERT INTO face_encodings (file_path, encoding) VALUES (%s, %s)",
                             (photo_path, encoding.tobytes()))
            dbCon.commit()
