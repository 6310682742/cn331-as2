from http.client import HTTPResponse
from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logout'),
    path('regist/', views.registUser, name='regist'),
    path('room/<str:pk>', views.room, name='room'),
    path('userprofile/', views.userProfile, name='userProfile'),
    path('course_form/',views.createCourse, name='course_form'),
    path('deleteCourse/<str:pk>', views.deleteCourse, name='deleteCourse'),
    path('editCourse/<str:pk>',views.editCourse, name='editCourse')
]