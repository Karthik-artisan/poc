import os
import face_recognition
import cv2
import numpy as np
import mysql.connector

# Connect to database
dbCon = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="firstdemo"
)
conn = dbCon.cursor()


# Function to retrieve face encodings from the database
def get_face_encodings():
    conn.execute("SELECT file_path, encoding FROM face_encodings")
    return conn.fetchall()


# Function to compare two face encodings and return a boolean value indicating if they match
def compare_face_encodings(encoding1, encoding2):
    encoding22 = np.frombuffer(encoding2, dtype=np.float64)
    return np.linalg.norm(encoding1 - encoding22) < 0.6

face_encodings = get_face_encodings()

# Loop through the face encodings and filter the photos to only include those that match
matching_photos = []
photo_image = cv2.imread('/Users/karthi/Photos/Selfie/selfie1.jpeg')
photo_image = cv2.cvtColor(photo_image, cv2.COLOR_BGR2RGB)
photo_encodings = face_recognition.face_encodings(photo_image)

for file_path, encoding in face_encodings:
    if len(photo_encodings) > 0:
        for face_encoding in photo_encodings:
            if compare_face_encodings(face_encoding, encoding):
                matching_photos.append(file_path)

print(matching_photos)
