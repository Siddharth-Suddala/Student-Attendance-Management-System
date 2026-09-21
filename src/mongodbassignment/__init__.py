import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")


class AttendanceManager:

    def __init__(self, connection_string, database_name):

        mongo_url = connection_string
        mongo_client = MongoClient(mongo_url)

        database = mongo_client[database_name]

        self.studentdata = database["studentdata"]
        self.attendancedata = database["attendancedata"]


    def add_student(self, name, roll_no, email, course):

        try:
            student = self.studentdata.find_one({
                "roll_no": roll_no
            })

            if student:
                print("Student with this roll number already exists")
                return

            student_data = {
                "name": name,
                "roll_no": roll_no,
                "email": email,
                "course": course
            }

            self.studentdata.insert_one(student_data)

            print("Student added")

        except PyMongoError:
            print("Database error occurred")


    def get_all_attendance(self):

        try:
            attendance_records = self.attendancedata.find()

            records = []

            for record in attendance_records:
                records.append(record)

            return records

        except PyMongoError:
            print("Database error occurred")
            return []


    def add_attendance(self, roll_no, date, status):

        if status not in ["Present", "Absent"]:
            print("Invalid attendance status")
            return

        try:
            student = self.studentdata.find_one({
                "roll_no": roll_no
            })

            if not student:
                print("Student does not exist")
                return

            attendance_data = {
                "roll_no": roll_no,
                "date": date,
                "status": status
            }

            self.attendancedata.insert_one(attendance_data)

            print("Attendance added")

        except PyMongoError:
            print("Database error occurred")


    def delete_student(self, roll_no):

        try:
            student = self.studentdata.find_one({
                "roll_no": roll_no
            })

            if not student:
                print("Nothing to delete. Student does not exist")
                return

            self.studentdata.delete_one({
                "roll_no": roll_no
            })

            print("Student deleted")

        except PyMongoError:
            print("Database error occurred")


attendancemgr = AttendanceManager(MONGO_URL, "college_data")


attendancemgr.add_student(
    "Raj", "CS001", "raj@gmail.com", "BTech CSE"
)


attendancemgr.add_student(
    "Rahul", "CS002", "rahul@gmail.com", "BTech CSE"
)


attendancemgr.add_attendance(
    "CS001", "2026-09-21", "Present"
)

attendancemgr.add_attendance(
    "CS002", "2026-09-21", "Absent"
)


print(attendancemgr.get_all_attendance())


attendancemgr.delete_student("CS002")