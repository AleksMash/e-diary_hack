from datacenter.models import (Schoolkid, Lesson,
                               Mark, Chastisement, Commendation)
import random as rnd


COMMENDATION_TEXT = ['Хвалю!',
                     'Отличная работа',
                     'Молодец!',
                     'Заслужил!',
                     'Так деражть!',
                     ]


def get_child(child_name):
    if not child_name:
        print('Необходимо указать фамилию и имя ученика')
        return
    try:
        return Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.MultipleObjectsReturned:
        print('Проверьте верно ли были указаны фамилия и имя ученика'
              ',так как были найдены несколько учеников,'
              'соответствующих заданным данным')
    except Schoolkid.DoesNotExist:
        print('В базе данных нет ученика с указанными именем и фамилией')


def fix_marks(child_name):
    child = get_child(child_name)
    if child:
        Mark.objects.filter(schoolkid=child, points__lte=3).update(points=5)


def remove_chastisements(child_name):
    child = get_child(child_name)
    if child:
        chastisements = Chastisement.objects.filter(schoolkid=child)
        chastisements.delete()


def create_commendation(child_name, subject_title):
    child = get_child(child_name)
    if child:
        lessons = Lesson.objects.filter(
            group_letter__contains=child.group_letter,
            year_of_study=child.year_of_study,
            subject__title=subject_title
        )
        if not lessons:
            print('Нет уроков по такому предмету, возможно вы '
                  'ошиблись в названия предмета')
            return
        lesson = rnd.choice(lessons)
        text = rnd.choice(COMMENDATION_TEXT)
        Commendation.objects.create(text=text, created=lesson.date,
                                    schoolkid=child, subject=lesson.subject,
                                    teacher=lesson.teacher)
