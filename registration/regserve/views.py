from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from rest_framework import generics
from django.views.generic import ListView, CreateView

def index(request):
    # Respond to requests
    return HttpResponse("Hello world from django backend")

class StudentListView(generics.ListCreateAPIView):
    # convert data sets
    queryset = Student.objects.all()
    # data serialization
    serializer_class = StudentSerializer

class StudentListForm(ListView):
    model = Student

class StudentCreateForm(CreateView, ListView):
    model = Student
    fields = ['firstname', 'lastname', 'idnumber', 'schoolyear', 'major', 'gpa']