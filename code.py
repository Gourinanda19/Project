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

try:
    lnwriter.writerow(["Names", "Time of Entrance"])

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,
                                                             face_locations)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings,
                                                         face_encoding,
                                                         tolerance=threshold)
                name = ""
                abc = known_face_encodings
                face_distances = face_recognition.face_distance(abc,
                                                                face_encoding)

                if min(face_distances) < 0.5:
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                else:
                    name = "Unknown"

                face_names.append(name)

                if name in face_names:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottomLeftCornerOfText = (10, 100)
                    fontScale = 1.5
                    fontColor = (255, 0, 0)
                    thickness = 3
                    lineType = 2
                    cv2.putText(frame, name,
                                bottomLeftCornerOfText,
                                font,
                                fontScale,
                                fontColor,
                                thickness,
                                lineType)

                    if name in students:
                        students.remove(name)
                        current_time = now.strftime("%H-%M-%S")
                        lnwriter.writerow([name, current_time])

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred during video processing: {e}")

finally:
    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

try:
    analyze_attendance("attendance_files/"+current_date + '.csv')
except Exception as e:
    print(f"Failed to analyze attendance: {e}")
