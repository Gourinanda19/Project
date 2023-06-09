import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime


# Function to analyze attendance data
def analyze_attendance(csv_file):
    global known_face_encodings
    # Open CSV file
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # leave the header row out
        next(reader)

        # Initialize variables for attendance analysis
        total_students = len(known_face_names)
        present_students = 0

        # Iterate through each row of CSV file
        for row in reader:
            name, timestamp = row

            # Check if student attended
            if timestamp != "":
                present_students += 1

        # Calculate the attendance percentage
        attendance_percentage = (present_students / total_students) * 100

        # Print the analysis results
        print("Attendance Analysis:")
        print(f"Total Students: {total_students}")
        print(f"Present Students: {present_students}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")


# Open video capture
try:
    video_capture = cv2.VideoCapture(0)
except Exception as e:
    print(f"Failed to open video capture: {e}")
    exit(1)

# Define the folder path where the images are located
folder_path = "pictures/"

# Initialize an empty list to store face encoding and names of individuals
known_face_encodings = []
known_face_names = []

# Recapitulate over files in  folder
for file_name in os.listdir(folder_path):
    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)

    try:
        # Download image file
        image = face_recognition.load_image_file(file_path)

        # Encode the face of individual
        encoding = face_recognition.face_encodings(image)

        # Ensure that at least one face is found in the image
        if len(encoding) > 0:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(file_name)[0])
        else:
            print(f"No face found in {file_name}")
    except Exception as e:
        print(f"Failed to process image {file_name}: {e}")

# Make a copy of known face names for attendance tracking
students = known_face_names.copy()

# Initialize some variables for the face detection
face_locations = []
face_encodings = []
face_names = []
s = True
threshold = 0.6

# Get the current date for CSV file name
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Open CSV file to enter  attendance data
try:
    f = open("attendance_files/"+current_date + '.csv', 'w+', newline='')
except Exception as e:
    print(f"Failed to open CSV file for writing: {e}")
    exit(1)

lnwriter = csv.writer(f)

try:
    lnwriter.writerow(["Names", "Time of Entrance"])

    # Main loop for capturing and processing video frames
    while True:
        # Read  frame of captured video
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame")
            break

        # Resize frame for rapid face identification
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if s:
            # Finding the locations and encoding of face in the frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,
                                                             face_locations)
            face_names = []

            for face_encoding in face_encodings:
                # Compare the encoding data with known faces
                matches = face_recognition.compare_faces(known_face_encodings,
                                                         face_encoding,
                                                         tolerance=threshold)
                name = ""
                abc = known_face_encodings
                face_distances = face_recognition.face_distance(abc,
                                                                face_encoding)

                # Find the perfect match
                if min(face_distances) < 0.5:
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                else:
                    name = "Unknown"

                face_names.append(name)

                if name in face_names:
                    # Draw bounding box and text on the frame
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
                        # Remove student from list once attendance is marked
                        students.remove(name)
                        # print(students)
                        current_time = now.strftime("%H-%M-%S")
                        lnwriter.writerow([name, current_time])

        # The frame should be displayed
        cv2.imshow("Attendance System", frame)

        # look for the 'q' key and press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred during video processing: {e}")

finally:
    # The captured video should be relased and close the windows
    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

# Analyze the attendance
try:
    analyze_attendance("attendance_files/"+current_date + '.csv')
except Exception as e:
    print(f"Failed to analyze attendance: {e}")

# Define the folder path where the attendance files are located
folder_path2 = "attendance_files/"

# Initialize a dictionary to store attendance counts per student
attendance_counts = {i: 0 for i in known_face_names}

# All the files in folder will be iterated
for file_name in os.listdir(folder_path2):
    # conform whether the file is  CSV file or not
    if file_name.endswith(".csv"):
        # To make a full file path
        file_path = os.path.join(folder_path2, file_name)

        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                # Pass over the header row
                next(reader)

                # Iterate through all rows of CSV file
                for row in reader:
                    name = row[0]  # Assume the student name is in first column

                    if name != "Names":  # Skip the header row
                        if name in attendance_counts:
                            attendance_counts[name] += 1
        except Exception as e:
            print(f"Failed to process attendance file {file_name}: {e}")


# Calculate attendance percentages
total_files = len(os.listdir(folder_path2))
attendance_percentages = {}
for name, count in attendance_counts.items():
    percentage = (count / total_files) * 100
    attendance_percentages[name] = percentage

# Print attendance percentages
print("Total attendance percentage of each student:")
for name, percentage in attendance_percentages.items():
    print(f"{name}: {percentage:.2f}%")
