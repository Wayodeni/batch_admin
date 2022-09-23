import csv
import requests


def get_subject_id_by_name_and_type(subject_dict: dict[str, str]) -> (int | None):
    query = {
        'name': subject_dict['name'],
        'subject_type': subject_dict['subject_type'],
    }
    response = requests.get(ROOT_URL + 'subject' + '/', params=query)
    try:
        return response.json()[0]['id']
    except:
        print('Subject not found: ')
        print('Subject URL: ' + response.url)
        print()

def get_subject_type_id_by_naming(subject_type):
    if subject_type == 'Лекция':
        return 0
    elif subject_type == 'Практика':
        return 1
    else:
        print('No corresponding subject type for ' + subject_type)
        print()

def get_group_id_by_name(group_name):
    query = {
        'name': group_name,
    }
    response = requests.get(ROOT_URL + 'student_group' + '/', params=query)
    try:
        return response.json()[0]['id']
    except:
        print('Group not found with URL:')
        print(response.url)
        print()

def get_teacher_id_by_full_name(teacher_object):
    query = {
        'first_name': teacher_object['first_name'],
        'middle_name': teacher_object['middle_name'],
        'last_name': teacher_object['last_name'],
    }
    response = requests.get(ROOT_URL + 'teacher' + '/', params=query)
    try:
        return response.json()[0]['id']
    except:
        print('Teacher not found with URL:')
        print(response.url)
        print()

def create_lesson(lesson_obj):
    response = requests.post(ROOT_URL + 'schedule' + '/', json=lesson_obj)
    # print('Creating: ', lesson_obj)
    # print('Lesson creation status:', response.text)
    # print()


ROOT_URL = 'http://localhost:8000/api/'
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

with open(FILE_PATH, 'r') as csv_file:
    reader = csv.reader(csv_file)

    for csv_row in reader:
        week_type = csv_row[WEEK_TYPE_COL]

        day_number = csv_row[DAY_NUMBER_COL]

        lesson_number = csv_row[LESSON_NUMBER_COL]
        subject_name = csv_row[LESSON_NAME_COL]
        subject_type_naming = csv_row[LESSON_TYPE_COL]

        group_name = csv_row[GROUP_NAME_COL]

        teacher_last_name = csv_row[TEACHER_SECOND_NAME_COL]
        teacher_first_name = csv_row[TEACHER_FIRST_NAME_COL]
        teacher_middle_name = csv_row[TEACHER_THIRD_NAME_COL]

        schedule_lesson_obj = {
            'week': '',
            'day': '',
            'lesson': '',
            'subject': '',
            'group': '',
            'teacher': '',
        }

        if week_type == 'верхняя':
            schedule_lesson_obj['week'] = '1'
        else:
            schedule_lesson_obj['week'] = '0'

        schedule_lesson_obj['day'] = day_number
        schedule_lesson_obj['lesson'] = lesson_number
        schedule_lesson_obj['group'] = get_group_id_by_name(group_name)
    
        schedule_lesson_obj['subject'] = get_subject_id_by_name_and_type({
            'name': subject_name,
            'subject_type': get_subject_type_id_by_naming(subject_type_naming),
        })
    
        schedule_lesson_obj['teacher'] = get_teacher_id_by_full_name({
            'first_name': teacher_first_name,
            'last_name': teacher_last_name,
            'middle_name': teacher_middle_name,
        })
    
        if not all(schedule_lesson_obj.values()):
            print('Some schedule_lesson_obj values are empty:')
            print(schedule_lesson_obj)
            print('Discarding POST to create')
        else:
            create_lesson(schedule_lesson_obj)
