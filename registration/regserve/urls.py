from django.urls import path

from . import views

application = 'regserve'

urlpatterns = [
    path('', views.index, name='index'),
    path('data/students/', views.StudentListView.as_view(), name = 'api_students'),
]
