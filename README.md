#Facial Recognition Attendance System#
#Description 
This project is a facial recognition attendance system that uses face recognition techniques to track and analyze attendance.The system captures video frames,identifies faces,and matches them against a pre-defined set of known faces.The attendance information is then stored in CSV files for further analysis.
#Preliminary Installations
• This code is written in Python 3.x , To run this project, we need the following libraries:
• face_recognition library
• cv2 (OpenCV) library
• numpy library
• openpyxl library (for attendance analysis)
!pip3 install face_recognition
!pip3 install opencv-python
!pip3 install numpy 
!pip3 install openpyxl
• Download or clone the project code from the GitHub repository << >>
#Usage
• Place the images of the known faces in the "pictures" folder. Each image should contain
only one face and the file name should correspond to the name of the person.
• Run "attendance_system" << name of the project >>
• The system will start capturing video frames from the default camera (index 0). It will try
to recognize faces in each frame and mark attendance if a known face is detected.
• Press 'q' to stop the attendance system and close the application.
• After running the attendance system, the attendance records for each day will be stored in
the "attendance_files" folder as CSV files. The file name format is "DATE.csv" (DATE is
in the format of YYYY-MM-DD )
•we have defined a function analyze_attendence which is used to calculate attendence percentage for each day.
• The analysis results will be printed, showing the total number of students, present
students, and attendance percentage.
#Note
The attendance system uses a threshold value of 0.6 for face recognition. You can modify this
value in the code to adjust the sensitivity of face matching & The system assumes that each
student's name is present in the first column of the CSV file generated for attendance records.




