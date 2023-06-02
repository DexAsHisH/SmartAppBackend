# build a schema using pydantic

from typing import Optional
from pydantic import BaseModel
from sqlalchemy import DateTime

#from sqlalchemy.dialects.postgresql import UUID


class Login(BaseModel):
    username: str
    password: str
    #email: str
    #name: str

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
    
    

    class Config:
       orm_mode = True    

class UserProfileResponse(BaseModel):
    userId: str
    username: str
    email: str
    

    class Config:
       orm_mode = True             


class Signup(BaseModel):
    username: str
    email: Optional[str]=None
    password: str

    class Config:
       orm_mode = True     

class SignupResponse(BaseModel):
    username: str

    class Config:
       orm_mode = True           


class Student(BaseModel):
    #student_id: str
    name: str
    roll_no: Optional[str]=None
    section: Optional[str]=None
    
    class Config:
       orm_mode = True
   
class StudentResponse(BaseModel):
    student_id: str
    name: str
    roll_no: Optional[str]=None
    section: Optional[str]=None
    
    class Config:
       orm_mode = True
   
class Attendence(BaseModel):
    #attendence_id: str
    student_id: str
    course_id: str
    classroom_id: str
    subject_id: str
    #date: str
    status: str

    class Config:
       orm_mode = True
 

class Subject(BaseModel):
    #subject_id: str
    name: str
    
    class Config:
       orm_mode = True
   
class SubjectResponse(BaseModel):
    subject_id: str
    name: str
    
    class Config:
       orm_mode = True
   
class Teacher(BaseModel):
    teacher_id: str
    name: str
    subject_id: str

    class Config:
       orm_mode = True
   


class Course(BaseModel):
    #course_id: str
    name: str
    semester: Optional[str]=None
    
    class Config:
       orm_mode = True
   
class CourseResponse(BaseModel):
    course_id: str
    name: str
    semester: Optional[str]=None
    
    class Config:
       orm_mode = True
   


class Classroom(BaseModel):
    classroom_id: str
    name: str
    building_name: Optional[str]=None
    
    class Config:
       orm_mode = True
   
