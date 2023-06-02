from operator import index
from tokenize import Number
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True, index=True)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    #firstName = Column(String(64), nullable=True, default='')
    #lastName = Column(String(64), nullable=True, default='')
    #phone = Column(Integer, nullable=True, default='')


class Student(Base):
    __tablename__ = 'students'
    student_id =Column(String, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    roll_no = Column(String(64), nullable=False)
    section = Column(String(64), nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id =Column(String, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    subject_id =Column(Integer, primary_key=True, index=True)


class Subject(Base):
    __tablename__ = 'subjects'
    subject_id =Column(String, primary_key=True, index=True)
    name = Column(String(64), nullable=False)

class Course(Base):
    __tablename__ ='courses'
    course_id =Column(String, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    semester = Column(String(64), nullable=False)

class Classroom(Base):
    __tablename__ ='classrooms'
    classroom_id =Column(String, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    building_name = Column(String(64), nullable=False)

class Attendence(Base):
    __tablename__ ='attendence'
    attendence_id =Column(String, primary_key=True, index=True)
    student_id =Column(String)
    course_id =Column(String)
    subject_id =Column(String)
    classroom_id =Column(String)
    #date =Column(Date,nullable=True)
    status =Column(String,nullable=False)





