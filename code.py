import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime


def analyze_attendance(csv_file):
    global known_face_encodings
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        next(reader)

        total_students = len(known_face_names)
        present_students = 0

        for row in reader:
            name, timestamp = row

            if timestamp != "":
                present_students += 1

        attendance_percentage = (present_students / total_students) * 100

        print("Attendance Analysis:")
        print(f"Total Students: {total_students}")
        print(f"Present Students: {present_students}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")


try:
    video_capture = cv2.VideoCapture(0)
except Exception as e:
    print(f"Failed to open video capture: {e}")
    exit(1)

folder_path = "pictures/"

known_face_encodings = []
known_face_names = []

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    try:
        image = face_recognition.load_image_file(file_path)

        encoding = face_recognition.face_encodings(image)

        if len(encoding) > 0:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(file_name)[0])
        else:
            print(f"No face found in {file_name}")
    except Exception as a:
        print(f"Failed to process image {file_name}: {a}")

students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True
threshold = 0.6

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

try:
    f = open("attendance_files/"+current_date + '.csv', 'w+', newline='')
except Exception as e:
    print(f"Failed to open CSV file for writing: {e}")
    exit(1)

lnwriter = csv.writer(f)


