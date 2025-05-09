from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    subjects = relationship('Subjects', back_populates='teacher')

class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE', onupdate='CASCADE'))
    teacher = relationship('Teachers', back_populates='subjects')
    grades = relationship('Grades', back_populates='subject')

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))
    group = relationship('Groups', back_populates='students')
    grades = relationship('Grades', back_populates='student')

class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    students = relationship('Students', back_populates='group')

class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grades = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE', onupdate='CASCADE'))
    date_of_grade = Column(Date, nullable=False)
    student = relationship("Students", back_populates="grades")
    subject = relationship("Subjects", back_populates="grades")