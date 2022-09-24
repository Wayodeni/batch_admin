import csv
import requests


def get_week_type_id_by_name(week_type_name: str) -> (str | None):
    if week_type_name == 'верхняя':
        return '1'
    elif week_type_name == 'нижняя':
        return '0'
    else:
        print('No corresponding week type id for ' + week_type_name)
        print()


def get_subject_id_by_name_and_type(subject_dict: dict[str, str]) -> (str | None):
    query = {
        'name': subject_dict['name'],
        'subject_type': subject_dict['subject_type'],
    }

    response = requests.get(ROOT_URL + 'subject' + '/', params=query)

    try:
        return str(response.json()[0]['id'])
    except:
        print('Subject not found: ')
        print('Subject URL: ' + response.url)
        print()


def get_subject_type_id_by_name(subject_type_name: str) -> (str | None):
    if subject_type_name == 'Лекция':
        return '0'
    elif subject_type_name == 'Практика':
        return '1'
    else:
        print('No corresponding subject type for ' + subject_type_name)
        print()


def get_group_id_by_name(group_name: str) -> (str | None):
    query = {
        'name': group_name,
    }

    response = requests.get(ROOT_URL + 'student_group' + '/', params=query)

    try:
        return str(response.json()[0]['id'])
    except:
        print('Group not found with URL:')
        print(response.url)
        print()


def get_teacher_id_by_full_name(teacher_object: dict[str, str]) -> (str | None):
    query = {
        'first_name': teacher_object['first_name'],
        'middle_name': teacher_object['middle_name'],
        'last_name': teacher_object['last_name'],
    }

    response = requests.get(ROOT_URL + 'teacher' + '/', params=query)
    
    try:
        return str(response.json()[0]['id'])
    except:
        print('Teacher not found with URL:')
        print(response.url)
        print()


def create_lesson(lesson_obj:dict[str, str]) -> None:
    if all(schedule_lesson_obj.values()):
        response = requests.post(ROOT_URL + 'schedule' + '/', json=lesson_obj)
        # print('Creating: ', lesson_obj)
        # print('Lesson creation status: ', response.text)
        # print()
    else:
        print('Some schedule_lesson_obj values are empty:')
        print(schedule_lesson_obj)
        print('Discarding POST to create')
        print('=============================================')




ROOT_URL = 'http://127.0.0.1:8000/api/'
FILE_PATH = 'setmag_lessons.csv'

WEEK_TYPE_NAME_COL = 0

DAY_ID_COL = 1

LESSON_ID_COL = 2
SUBJECT_NAME_COL = 3
SUBJECT_TYPE_NAME_COL = 4

GROUP_NAME_COL = 5

TEACHER_LAST_NAME_COL = 6
TEACHER_FIRST_NAME_COL = 7
TEACHER_MIDDLE_NAME_COL = 8

with open(FILE_PATH, 'r', encoding='utf-8') as csv_file:
    data = csv.reader(csv_file)

    for csv_row in data:
        week_type_name = csv_row[WEEK_TYPE_NAME_COL]

        day_id = csv_row[DAY_ID_COL]

        lesson_id = csv_row[LESSON_ID_COL]
        subject_name = csv_row[SUBJECT_NAME_COL]
        subject_type_name = csv_row[SUBJECT_TYPE_NAME_COL]

        group_name = csv_row[GROUP_NAME_COL]

        teacher_last_name = csv_row[TEACHER_LAST_NAME_COL]
        teacher_first_name = csv_row[TEACHER_FIRST_NAME_COL]
        teacher_middle_name = csv_row[TEACHER_MIDDLE_NAME_COL]

        schedule_lesson_obj = {
            'week': '',
            'day': '',
            'lesson': '',
            'subject': '',
            'group': '',
            'teacher': '',
        }

        schedule_lesson_obj['week'] = get_week_type_id_by_name(week_type_name)
        schedule_lesson_obj['day'] = day_id if int(day_id) in range(1, 8) else print('Wrong day id: ', day_id)
        schedule_lesson_obj['lesson'] = lesson_id if int(lesson_id) in range(1, 8) else print('Wrong lesson id: ', lesson_id)
        schedule_lesson_obj['subject'] = get_subject_id_by_name_and_type({
            'name': subject_name,
            'subject_type': get_subject_type_id_by_name(subject_type_name),
        })
        schedule_lesson_obj['group'] = get_group_id_by_name(group_name)
        schedule_lesson_obj['teacher'] = get_teacher_id_by_full_name({
            'first_name': teacher_first_name,
            'last_name': teacher_last_name,
            'middle_name': teacher_middle_name,
        })

        create_lesson(schedule_lesson_obj)
