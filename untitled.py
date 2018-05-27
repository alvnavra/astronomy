import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.testdb
student1 = {"name": "Arun",
            "classid": 'V',
		"rollno": 1}
students = db.students
students_id = students.insert(student1)
students_id