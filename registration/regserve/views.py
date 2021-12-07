from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from rest_framework import generics

def index(request):
    return HttpResponse("Hello world from django backend")

class StudentListView(generics.ListCreateAPIView):
    student_list = Student.objects.all()
    serializer_class = StudentSerializer