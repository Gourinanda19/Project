# Facial Recognition Attendance System
## Description 
This project is a facial recognition attendance system that uses face recognition techniques to track and analyze attendance. The system captures video frames,identifies faces,and matches them against a pre-defined set of known faces. The attendance information is then stored in CSV files for further analysis.
## Preliminary Installations
This code is written in Python 3.x. To run this project, we need the following libraries:
* face_recognition library
* cv2 (OpenCV) library
* numpy library
* csv module
* os module
* datetime module

## Usage
* Place the images of the known faces in the "pictures" folder. Each image should contain
only one face and the file name should correspond to the name of the person.
* Run "attendance_system" << name of the project >>
* The system will start capturing video frames from the default camera (index 0). It will try
to recognize faces in each frame and mark attendance if a known face is detected.
* Press 'q' to stop the attendance system and close the application.
* After running the attendance system, the attendance records for each day will be stored in
the "attendance_files" folder as CSV files. The file name format is "DATE.csv" (DATE is
in the format of YYYY-MM-DD )
* We have defined a function analyze_attendence which is used to calculate attendence percentage of the class for each day.
* The analysis results will be printed, showing the total number of students, present
students, and attendance percentage.

## Note
The attendance system uses a threshold value of 0.6 for face recognition. You can modify this
value in the code to adjust the sensitivity of face matching.

## Team Members
* Gourinanda R
* K Priyamvada
* Akhila

## References
The code that we further modified: https://i-know-python.com/facial-recognition-attendance-system-using-python/

The youtube link we referred: https://www.youtube.com/watch?v=A6464U4bPPQ

Other sites which were referred include:
* https://www.geeksforgeeks.org/how-to-install-face-recognition-in-python-on-windows/
* https://pypi.org/project/face-recognition/
*  https://docs.python.org/3/library/csv.html
*  https://www.geeksforgeeks.org/numpy-in-python-set-1-introduction/



