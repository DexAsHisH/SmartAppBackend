# build a schema using pydantic
from pydantic import BaseModel
#from sqlalchemy.dialects.postgresql import UUID


class Login(BaseModel):
    username: str
    password: str

    class Config:
       orm_mode = True


class LoginResponse(BaseModel):
    #userid: str
    username: str
    email: str
    #firstName: str
    #lastName: str


    class Config:
       orm_mode = True   


class UserProfile(BaseModel):
    id: str
    class Config:
       orm_mode = True       


class UserDetails(BaseModel):
    userId: str
    username: str
    password: str
    email: str
    firstName: str
    lastName: str
    phone: str
    

    class Config:
       orm_mode = True    

class UserProfileResponse(BaseModel):
    userId: str
    username: str
    email: str
    firstName: str
    lastName: str
    phone: str
    

    class Config:
       orm_mode = True             

class Signup(BaseModel):
    username: str
    email: str
    password: str

    class Config:
       orm_mode = True     

class SignupResponse(BaseModel):
    username: str

    class Config:
       orm_mode = True           