import csv
import requests


def create_group_by_name(group_name):
    requests.post(ROOT_URL + 'student_group' + '/', json=group_name)


ROOT_URL = 'http://localhost:8000/api/'
FILE_PATH = 'temp.csv'

with open(FILE_PATH, 'r', encoding='utf-8') as csv_file:
    data = csv.reader(csv_file)

    for csv_row in data:
        create_group_by_name(csv_row[0])
