ROOT_URL = 'http://schedule.miigaik.ru/api/'
FILE_PATH = 'setmag_lessons.csv'

WEEK_TYPE_COL = 0

DAY_NUMBER_COL = 1

LESSON_NUMBER_COL = 2
LESSON_NAME_COL = 3
LESSON_TYPE_COL = 4

GROUP_NAME_COL = 5

TEACHER_SECOND_NAME_COL = 6
TEACHER_FIRST_NAME_COL = 7
TEACHER_THIRD_NAME_COL = 8


import csv
import requests


def get_lesson_id(subject_object):
    query = {
        'name': subject_object['name'],
        'subject_type': subject_object['subject_type'],
    }
    response = requests.get(ROOT_URL + 'subject' + '/', params=query)
    try:
        return response.json()[0]['id']
    except:
        print('Lesson not found')
        print(response.url)

def get_subject_type_numeral(subject_type):
    if subject_type == 'Лекция':
        return 0
    elif subject_type == 'Практика':
        return 1
    else:
        return 'No corresponding subject type for ' + subject_type

def get_group_id(group_name):
    query = {
        'name': group_name,
    }
    response = requests.get(ROOT_URL + 'student_group' + '/', params=query)
    return response.json()[0]['id']

def get_teacher_id(teacher_object):
    query = {
        'first_name': teacher_object['first_name'],
        'middle_name': teacher_object['third_name'],
        'last_name': teacher_object['second_name'],
    }
    response = requests.get(ROOT_URL + 'teacher' + '/', params=query)
    try:
        return response.json()[0]['id']
    except:
        print('Teacher not found with URL:')
        print(response.url)
        print('Setting teacher object to None')

def create_lesson(lesson_obj):
    print(lesson_obj)
    response = requests.post(ROOT_URL + 'schedule' + '/', json=lesson_obj)
    print('Lesson creation status:', response.text)


with open(FILE_PATH, 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        lesson_obj = {
            'week': '',
            'day': '',
            'lesson': '',
            'subject': '',
            'group': '',
            'teacher': '',
        }
        for col in range(len(row)):
            cell_value = row[col]
            if col == WEEK_TYPE_COL:
                if cell_value == 'верхняя':
                    lesson_obj['week'] = '1'
                else:
                    lesson_obj['week'] = '0'
            elif col == DAY_NUMBER_COL:
                lesson_obj['day'] = cell_value
            elif col == LESSON_NUMBER_COL:
                lesson_obj['lesson'] = cell_value
            elif col == GROUP_NAME_COL:
                lesson_obj['group'] = get_group_id(row[GROUP_NAME_COL])
        lesson_obj['subject'] = get_lesson_id(
            {
                'name': row[LESSON_NAME_COL],
                'subject_type': get_subject_type_numeral(row[LESSON_TYPE_COL]),
            }
        )
        lesson_obj['teacher'] = get_teacher_id(
            {
                'first_name': row[TEACHER_FIRST_NAME_COL],
                'second_name': row[TEACHER_SECOND_NAME_COL],
                'third_name': row[TEACHER_THIRD_NAME_COL],
            }
        )
        
        for key in lesson_obj.keys():
            if not lesson_obj[key]:
                lesson_obj = None
        
        if lesson_obj:
            create_lesson(lesson_obj)
                
        #print(lesson_obj)







# print(get_teacher_id(
#     {
#         'first_name': 'Сергей',
#         'second_name': 'Александрович',
#         'third_name': 'Атаманов',
#     }
# ))
