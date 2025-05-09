from sqlalchemy.exc import SQLAlchemyError

from conf.models import Teachers, Subjects, Students, Groups, Grades
from conf.db import session
from faker import Faker
from random import randint, choice

faker = Faker('uk_UA')

def group_add():
    print('group_add start')
    for i in range(3):
        group = Groups(name=f"КІ-{i + 1}")
        session.add(group)
    print('group_add end')


def student_add():
    print('student_add start')
    for _ in range(50):
        student = Students(name=faker.name(), group_id=randint(1, 3))
        session.add(student)
    print('student_add end')


def teacher_add():
    print('teacher_add start')
    for _ in range(5):
        teacher = Teachers(name=faker.name())
        session.add(teacher)
    print('teacher_add end')


def subject_add():
    print('subject_add start')
    for _ in range(8):
        subject = Subjects(name=faker.word().capitalize(), teacher_id=randint(1, 5))
        session.add(subject)
    print('subject_add end')


def grade_add():
    print('grade_add start')
    students = session.query(Students).all()
    subjects = session.query(Subjects).all()
    if not students or not subjects:
        print("Когось не вистачає")
        return
    for student in students:
        for _ in range(randint(5, 15)):
            random_subject = choice(subjects)
            grade = Grades(grades=randint(20, 100), student_id=student.id, subject_id=random_subject.id,
                           date_of_grade=faker.date_between(start_date='-1y'))
            session.add(grade)
    print('grade_add end')

if __name__ == '__main__':
    try:
        group_add()
        student_add()
        teacher_add()
        subject_add()
        session.commit()
        print('Перший коміт')
        grade_add()
        session.commit()
        print('Другий коміт')
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        print('Кінець')
        session.close()