from datacenter.models import *
import random as rnd
from django.core.exceptions import (MultipleObjectsReturned,
                                    ObjectDoesNotExist)


commendation_text=['Хвалю!',
                   'Отличная работа',
                   'Молодец!',
                   'Заслужил!',
                   'Так деражть!',
                   ]


def fix_marks(child_name):
    if not child_name:
        print('Необходимо указать фамилию и имя ученика')
        return
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except MultipleObjectsReturned:
        print('Проверьте верно ли были указаны Фамилия и имя ученика'
              ',так как было обнаружено несколько учеников,'
              'соответствующих заданным данным')
    except ObjectDoesNotExist:
        print('В базе данных нет ученика с указанными именем и фаилией')
    else:
        bad_marks = Mark.objects.filter(schoolkid=child, points__lte=3)
        for mark in bad_marks:
            mark.points = 5
            mark.save()


def remove_chastisements(child_name):
    if not child_name:
        print('Необходимо указать фамилию и имя ученика')
        return
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except MultipleObjectsReturned:
        print('Проверьте верно ли были указаны Фамилия и имя ученика'
              ',так как было обнаружено несколько учеников,'
              'соответствующих заданным данным')
    except ObjectDoesNotExist:
        print('В базе данных нет ученика с указанными именем и фаилией')
    else:
        chastisements = Chastisement.objects.filter(schoolkid=child)
        chastisements.delete()


def create_commendation(child_name, subject_title):
    if not child_name:
        print('Необходимо указать фамилию и имя ученика')
        return
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except MultipleObjectsReturned:
        print('Проверьте верно ли были указаны Фамилия и имя ученика'
              ',так как было обнаружено несколько учеников,'
              'соответствующих заданным данным')
    except ObjectDoesNotExist:
        print('В базе данных нет ученика с указанными именем и фаилией')
    else:
        lessons = Lesson.objects.filter(group_letter__contains=child.group_letter,
                                       year_of_study=child.year_of_study,
                                       subject__title=subject_title)
        if not lessons:
            print('Нет уроков по такому предмету, возможно вы '
                  'ошиблись в названия предмета')
            return
        lesson = lessons[rnd.randint(0,len(lessons)-1)]
        text = commendation_text[rnd.randint(0,len(commendation_text)-1)]
        Commendation.objects.create(text=text, created=lesson.date,
                                    schoolkid=child, subject=lesson.subject,
                                    teacher=lesson.teacher)
