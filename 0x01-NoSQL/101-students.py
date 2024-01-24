#!/usr/bin/env python3
'''Students sorted by average score'''
from pymongo import MongoClient

list_all = __import__('8-all').list_all


def top_students(mongo_collection):
    '''Returns all students sorted by average score'''
    students = list(list_all(mongo_collection))
    for student in students:
        score = 0
        for topic in student.get('topics'):
            score += topic.get('score')
        student['averageScore'] = score / len(student.get('topics'))
    sorted_students = sorted(students, key=lambda x: x['averageScore'],
                             reverse=True)
    return sorted_students

