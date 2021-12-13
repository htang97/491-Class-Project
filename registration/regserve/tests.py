from django.test import TestCase, Client
from .serializers import *
from .models import *
import io
from rest_framework.parsers import JSONParser

import logging

# step 1, creating logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # info

# step 2, creating a handler, write log file
logfile = './log.txt'
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.DEBUG)

# step 3, creating another handler, output log to the console
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# step 4, output formatting
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# step 5, add logger to the handler
logger.addHandler(fh)
logger.addHandler(ch)



class DataTest(TestCase):
    def setUp(self):
        # creating test data student1
        student1 = Student.objects.create(
            firstname="First",
            lastname="Student",
            idnumber=100,
            email="first@student.edu",
            schoolyear="FR",
            major="CS",
            gpa=4.0,
            )
        # creating test data student2
        student2 = Student.objects.create(
            firstname="Second",
            lastname="Student",
            idnumber=101,
            email="second@student.edu",
            schoolyear="SR",
            major="ENG",
            gpa=2.0,
            )
        # the client for testing
        # initializing Client()
        self.test_client = Client()
        
    def test_student_api(self):
        # get the student data
        students_response = self.test_client.get('/regserve/data/students/')
        logger.info(f'\nTEST_STUDENT_API: api response is: {students_response} and the status is {students_response.status_code}')
        # check the if the response is 200
        self.assertEqual(students_response.status_code, 200)
        logger.info(f'\nTEST_STUDENT_API: api response content is: {students_response.content}')
        # convert students_response.content to stream
        student_stream = io.BytesIO(students_response.content)
        logger.info(f'\nTEST_STUDENT_API: api response content is: {student_stream}')
        # convert to JSON
        student_data = JSONParser().parse(student_stream)
        # get student 1 json data
        first_student_data = student_data[0]
        logger.info(f'\nTEST_STUDENT_API: api response data is: {student_data} and its id is {first_student_data["id"]}')
        # get the first student data from Student.objects
        first_student_db = Student.objects.get(id=student_data[0]['id'])
        logger.info(f'\nTEST_STUDENT_API: api response student object from DB is: {first_student_db}')
        # student data serialization
        first_student_serializer = StudentSerializer(first_student_db, data=first_student_data)
        logger.info(f'\nTEST_STUDENT_API: api response student serializer is : {first_student_serializer}')
        logger.info(f'\nTEST_STUDENT_API: api response student serializer validity is : {first_student_serializer.is_valid()}')
        logger.info(f'\nTEST_STUDENT_API: api response student serializer validity is : {first_student_serializer.validated_data}')
        # save
        first_student_api = first_student_serializer.save()
        logger.info(f'\nTEST_STUDENT_API: api response student api object is : {first_student_api}')
        # check if the result is true
        self.assertEqual(first_student_db, first_student_api)

        

    def test_student(self):
        # get student list
        student_list = Student.objects.all()
        # get the first student
        student = student_list[0]
        logger.info(f'Inside test student: student is {student}')
        # check if the id is correct
        self.assertEqual(student.id, 1)
        # check if the full_name is correct
        self.assertEqual(student.full_name, 'First Student')
        # check if the idnumber is correct
        self.assertEqual(student.idnumber, 100)


class SimpleTest(TestCase):
    def setUp(self):
        # the client for testing
        self.test_client = Client()

    def test_response(self):
        # get the views data
        response = self.test_client.get('/regserve/')
        # check if the request is successful
        self.assertEqual(response.status_code, 200)
        # output
        self.assertEqual(response.content, b"Hello world from django backend")
