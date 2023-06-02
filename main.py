
# from threading import Thread

from typing import Optional,List

import os
import uuid
from fastapi import FastAPI, HTTPException,WebSocket
from fastapi_socketio import SocketManager
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


#Schemas
from schema import Login, Student,Attendence,Classroom,Course,Subject, SubjectResponse
from schema import LoginResponse
from schema import Signup
from schema import SignupResponse
from schema import UserProfileResponse
from schema import UserProfile
from schema import UserDetails

#Models
from models import Users as UsersModel
from models import Student as StudentModel
from models import Teacher as TeacherModel
from models import Subject as SubjectModel
from models import Classroom as ClassroomModel
from models import Course as CourseModel
from models import Attendence as AttendenceModel

load_dotenv('.env')

app = FastAPI()
socket_manager = SocketManager(app=app, cors_allowed_origins=[])

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

CONNECTED_CLIENTS = {}

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/signup", response_model=SignupResponse)
def usersignup(user: Signup):

    user_id = uuid.uuid4();
    user = UsersModel(username=user.username,email=user.email,password=user.password,user_id=user_id)
    student = StudentModel(student_id=user_id)

    print("++++++++++++++++++++")
    print(user)
    db.session.add(user)
    db.session.commit()
    db.session.add(student)
    db.session.commit()
    return user



@app.post("/login", response_model=LoginResponse)
def userlogin(user: Login):
    result = db.session.query(UsersModel).filter(UsersModel.username == user.username).first()

    if(result):
        if(result.password == user.password):
            if result.username:
                username = result.username
            else:
                username = ''

            if result.email:
                email = result.email
            else:
                email = ''


            return {'username': result.username,'userid': result.user_id, 'email': email}
        else:
            raise HTTPException(status_code=400, detail="invalid username or password")
    else:
        raise HTTPException(status_code=400, detail="invalid username or password")      



@app.post("/user_detail/", response_model=Student)
async def create_student(student: Student):
        result = db.session.query(UsersModel).filter(UsersModel.user_id == student.student_id).first()

        
        if (result):
            update_student=db.session.query(StudentModel).filter(StudentModel.student_id == student.student_id).first()
            update_student.name=student.name
            update_student.roll_no=student.roll_no
            update_student.section=student.section
            db.session.commit() 

            return update_student
        else:
            return {"message": "Student not found"}
        

@app.get("/students/{student_id}")
async def get_student(student_id: str):
        result = db.session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        
        if (result):
            return {'name': result.name,'roll_no': result.roll_no,'section': result.section}
        else:
            return {"message": "Student not found"}
        

@app.post("/subjects/",response_model=SubjectResponse)
async def create_subject(subject: Subject):
     
    subject_id = uuid.uuid4();
    subject = SubjectModel(name=subject.name,subject_id=subject_id)
    db.session.add(subject)
    db.session.commit()
    return {'name': subject.name}



@app.get("/subjects/{subject_id}")
async def get_subject(subject_id: str):
        result = db.session.query(SubjectModel).filter(SubjectModel.subject_id == subject_id).first()
        
        if (result):
            return {'name': result.name}
        else:
            return {"message": "subject not found"}
        


@app.post("/courses/",response_model=Course)
async def create_course(course: Course):

    course_id = uuid.uuid4();
    course = CourseModel(name=course.name,course_id=course_id,semester=course.semester)
    db.session.add(course)
    db.session.commit()
    return course
    

@app.get("/courses/{course_id}")
async def get_course(course_id: str):
        result = db.session.query(CourseModel).filter(CourseModel.course_id == course_id).first()
        
        if (result):
            return {"message": "course found"}
        else:
            return {"message": "course not found"}
        

@app.post("/classrooms/",response_model=Classroom)
async def get_classroom(classroom: Classroom):
        
    classroom_id = uuid.uuid4();
    classroom = ClassroomModel(name=classroom.name,classroom_id=classroom_id)
    db.session.add(classroom)
    db.session.commit()
    return classroom


@app.get("/classrooms/{classroom_id}")
async def get_classroom(classroom_id: str):
        result = db.session.query(ClassroomModel).filter(ClassroomModel.classroom_id == classroom_id).first()
        
        if (result):
            return {"message": "classroom found"}
        else:
            return {"message": "classroom not found"}
        

@app.put("/attendence/",response_model=Attendence)
async def update_attendence(attendence: Attendence):
           
            attendence_id = uuid.uuid4();
            attended = AttendenceModel(student_id=attendence.student_id,attendence_id=attendence_id,subject_id=attendence.subject_id,course_id=attendence.course_id,classroom_id=attendence.classroom_id,status=attendence.status)
            db.session.add(attended)
            db.session.commit()

            return attendence
  
        


@app.get("/attendence/{student_id}")
async def get_attendence(student_id: str):
        result = db.session.query(AttendenceModel).filter(AttendenceModel.student_id == student_id).first()

        if (result):
            return {"message": "record found"}
        else:
            return {"message": "record not found"}


@app.get("/attendance/{student_id}")
async def get_attendance(student_id: str):
    attendance_records = db.session.query(AttendenceModel).filter(AttendenceModel.student_id == student_id).all()

    if attendance_records:
        present_days = 0

        for record in attendance_records:
            if record.status == "present":
                present_days += 1

        return {"message": "Record found", "days_present": present_days}
    else:
        return {"message": "Record not found"}

#subject,course,classroon,attendance->get and put,
        



