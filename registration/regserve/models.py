from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.expressions import F

class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    idnumber = models.PositiveBigIntegerField()
    email = models.EmailField(blank=True)
    datecreated = models.DateTimeField(blank=True, auto_now_add=True)
    datemodified = models.DateTimeField(blank=True, auto_now=True)

    @property
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        abstract = True

    def __str__(self):
        return f'ID: {self.id}: name: {self.full_name}, studet id: {self.idnumber}, email: {self.email}, date created: {self.datecreated}, date modified: {self.datemodified}'

class Student(Person):
    YEAR_IN_SCHOOL = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]

    MAJORS = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('BUS', 'Business'),
        ('SC', 'Science'),
        ('LAW', 'Law'),
        ('NUR', 'Nursing'),
    ]
    schoolyear = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL)
    major = models.CharField(max_length=3, choices=MAJORS)
    gpa = models.FloatField(max_length=4, blank=True)

    def __str__(self):
        return f'StudentID: {self.id}: {super(Student, self).__str__()} - year in school: {self.schoolyear}, major: {self.major}, gpa: {self.gpa}'

    