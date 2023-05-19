
# from threading import Thread

from typing import Optional,List

import os
from fastapi import FastAPI, HTTPException,WebSocket
from fastapi_socketio import SocketManager
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


#Schemas
from schema import Login
from schema import LoginResponse
from schema import Signup
from schema import SignupResponse
from schema import UserProfileResponse
from schema import UserProfile
from schema import UserDetails

#Models
from models import Users as UsersModel


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
    db_user = UsersModel(username=user.username,email=user.email,password=user.password,user_id='e8d03d08-c309-4de2-bf38-dd65e4296b78')
    print("++++++++++++++++++++")
    print(db_user)
    db.session.add(db_user)
    db.session.commit()
    return db_user



@app.post("/login", response_model=LoginResponse)
def userlogin(user: Login):
    result = db.session.query(UsersModel).filter(UsersModel.username == user.username).first()

    if(result):
        if(result.password == user.password):
            if result.firstName:
                firstName = result.firstName
            else:
                firstName = ''

            if result.lastName:
                lastName = result.lastName
            else:
                lastName = ''

            if result.email:
                email = result.email
            else:
                email = ''


            return {'username': result.username,'userid': result.id, 'email': email, 'firstName': firstName, 'lastName': lastName}
        else:
            raise HTTPException(status_code=400, detail="invalid username or password")
    else:
        raise HTTPException(status_code=400, detail="invalid username or password")       






