
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
from schema import Login, Student,Attendence,Classroom,Course,Subject
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
    name ="Ashish Dabral"
    roll_no = "11"
    section = "A"
    user = UsersModel(username=user.username,email=user.email,password=user.password,user_id=user_id)
    student = StudentModel(student_id=user_id,name=name,roll_no=roll_no,section=section)

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



@app.get("/students/{student_id}")
async def get_student(student_id: str):
        result = db.session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
        print(student_id)
        if (result):
            return {"message": "Student found"}
        else:
            return {"message": "Student not found"}
        


@app.get("/subjects/{subject_id}")
async def get_student(subject_id: str):
        result = db.session.query(SubjectModel).filter(SubjectModel.subject_id == subject_id).first()
        print(subject_id)
        if (result):
            return {"message": "subject found"}
        else:
            return {"message": "subject not found"}
        

@app.get("/courses/{course_id}")
async def get_student(course_id: str):
        result = db.session.query(CourseModel).filter(CourseModel.course_id == course_id).first()
        print(course_id)
        if (result):
            return {"message": "course found"}
        else:
            return {"message": "course not found"}
        

@app.get("/classrooms/{classroom_id}")
async def get_student(classroom_id: str):
        result = db.session.query(ClassroomModel).filter(ClassroomModel.classroom_id == classroom_id).first()
        print(classroom_id)
        if (result):
            return {"message": "classroom found"}
        else:
            return {"message": "classroom not found"}
        

@app.put("/attendence/{attendence_id}")
async def get_student(attendence_id: str,attendence: Attendence):
        attend = db.session.query(AttendenceModel).filter(AttendenceModel.attendence_id == attendence_id).first()
        print(attendence_id)
        if (attend):
            attendence.status=True
            return {"message": "class attended"}
        else:
            return {"message": "class not attended"}
        

@app.get("/attendence/{attendence_id}")
async def get_student(attendence_id: str):
        result = db.session.query(AttendenceModel).filter(AttendenceModel.attendence_id == attendence_id).first()
        print(attendence_id)
        if (result):
            return {"message": "Student found"}
        else:
            return {"message": "Student not found"}
        


#subject,course,classroon,attendance->get and put,
        



