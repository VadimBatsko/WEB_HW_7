from sqlalchemy import func
from sqlalchemy import and_, or_, not_

from conf.models import Teachers, Subjects, Students, Groups, Grades
from conf.db import session


def select_1():
    five = session.query(Students, func.avg(Grades.grades)).join(Grades).group_by(
        Students.id).order_by(
        func.avg(Grades.grades).desc()).limit(5).all()
    return five


def select_2(subject_id):
    result = session.query(Students, func.avg(Grades.grades), Subjects.name). \
        join(Grades, Students.id == Grades.student_id). \
        join(Subjects, Grades.subject_id == Subjects.id). \
        filter(Subjects.id == subject_id). \
        group_by(Students.id, Students.name, Subjects.name). \
        order_by(func.avg(Grades.grades).desc()). \
        first()
    return result


def select_3(subject_id, group_id):
    result = session.query(func.avg(Grades.grades), Groups.name). \
        join(Students, Students.id == Grades.student_id). \
        join(Subjects, Grades.subject_id == Subjects.id). \
        join(Groups, Students.group_id == Groups.id). \
        filter((Subjects.id == subject_id) & (Groups.id == group_id)). \
        group_by(Groups.name). \
        first()
    return result


def select_4():
    result = session.query(func.avg(Grades.grades)).scalar()
    return result


def select_5(teacher_id):
    result = session.query(Teachers.name, Subjects.name).join(Subjects, Subjects.teacher_id == Teachers.id,
                                                              isouter=True).filter(Teachers.id == teacher_id).all()
    return result


def select_6(gro):
    result = session.query(Students.name, Groups.name).join(Groups, Groups.id == Students.group_id).filter(
        Groups.id == gro).all()
    return result


def select_7(gro_id, sub_id):
    result = session.query(Students.name, Groups.name, Subjects.name). \
        join(Groups, Groups.id == Students.group_id). \
        join(Grades, Students.id == Grades.student_id). \
        join(Subjects, Grades.subject_id == Subjects.id). \
        filter((Groups.id == gro_id) & (Subjects.id == sub_id)).all()
    return result


def select_8(teacher_id):
    result = session.query(Teachers.name, Subjects.name, func.avg(Grades.grades)) \
        .join(Teachers, Subjects.teacher_id == Teachers.id) \
        .join(Grades, Subjects.id == Grades.subject_id) \
        .filter(Teachers.id == teacher_id).group_by(Teachers.name, Subjects.name).all()
    return result


def select_9(st_id):
    result = session.query(Students.name, Subjects.name). \
        join(Grades, Students.id == Grades.student_id). \
        join(Subjects, Grades.subject_id == Subjects.id). \
        filter(Students.id == st_id). \
        group_by(Students.name, Subjects.name). \
        all()
    return result


def select_10(st_id, te_id):
    '''Список предметів, які певному студенту читає певний викладач.'''
    result = session.query(Students.name, Subjects.name, Teachers.name). \
        join(Grades, Grades.subject_id == Subjects.id). \
        join(Students, Students.id == Grades.student_id). \
        join(Teachers, Teachers.id == Subjects.teacher_id). \
        filter(Students.id == st_id, Teachers.id == te_id). \
        group_by(Students.name, Subjects.name, Teachers.name). \
        all()
    return result


def select_11(st_id, te_id):
    '''Середній бал, який певний викладач ставить певному студентові.'''
    result = session.query(Students.name, func.avg(Grades.grades), Teachers.name). \
        join(Grades, Students.id == Grades.student_id). \
        join(Subjects, Subjects.id == Grades.subject_id). \
        join(Teachers, Teachers.id == Subjects.teacher_id). \
        filter(Students.id == st_id, Teachers.id == te_id). \
        group_by(Students.name, Teachers.name). \
        all()
    return result

def select_12(g_id, su_id):
    '''Оцінки студентів у певній групі з певного предмета на останньому занятті.'''
    subquery = session.query(func.max(Grades.date_of_grade).label('last_lesson_date')). \
        join(Students, Students.id == Grades.student_id). \
        filter(Students.group_id == g_id, Grades.subject_id == su_id). \
        scalar_subquery()

    result = session.query(Students.name, Subjects.name, Grades.grades, Grades.date_of_grade). \
        join(Subjects, Subjects.id == Grades.subject_id). \
        join(Students, Students.id == Grades.student_id). \
        filter(Students.group_id == g_id, Subjects.id == su_id, Grades.date_of_grade == subquery). \
        all()
    return result

if __name__ == '__main__':

    result = select_12(2, 4)
    if result:
        student_name = result[0][0] if result else None
        print(f"Предмети, які вивчає студент {student_name}:")
        for row in result:
            print(f"{row[0]} - {row[1]} - {row[2]} - {row[3]}")
    else:
        print(f"Не знайдено інформації для студента з ID ")

    session.close()
