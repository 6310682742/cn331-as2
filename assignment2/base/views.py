from pydoc import describe
import re
from django.http import HttpResponse
from multiprocessing import context
from xml.etree.ElementTree import QName
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Course
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
# Create your views here.

def home(request):
    is_admin = request.user.is_superuser
    q = request.GET.get('q') if request.GET.get('q') != None else 'All'
    
    if q == "All":
        courses = Course.objects.all()
    elif q == "Open":
        courses = Course.objects.filter(course_status=True)
    elif q == "Closed":
        courses = Course.objects.filter(course_status=False)
    elif q == "Registered":
        courses = Course.objects.filter(student=request.user)
    elif q == "Available":
        courses = []
        for c in Course.objects.filter(course_status=True):
            courses.append(c)
    roomStatus = (
        "All",
        "Available",
        "Open",
        "Closed",
        "Registered",
        )
    user = request.user
    # print(user.username)
    context = {
        'courses':courses,
        'roomStatus':roomStatus,
        'q':q,
        'is_admin':is_admin,
        'user':user,

    }
    return render(request, 'base/home.html', context)
def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.object.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User does not exist')
    context = {}
    return render(request,'base/login.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')
def registUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'registration fail')
    return render(request, 'base/regist.html', {'form':form})
@login_required(login_url='login')
def room(request,pk):
    room = Course.objects.get(id=pk)
    describetion = room.describetion
    func = ""
    students = ""
    registable = request.user.is_superuser or request.user == room.teacher
    is_teacher = request.user == room.teacher
    # print(registable)
    if request.user.is_superuser:
        students = room.student.all()
    else:
        if(request.user in room.student.all()):
            func = "unregist"
        else:
            func = "regist"
        
        if request.method == 'POST':
            if request.user not in room.student.all():
                # print(room.max_student > len(room.student.all()))
                if room.course_status == True and room.max_student > len(room.student.all()):
                    room.student.add(request.user)
                else:
                    return HttpResponse("You can not register this couse because this couse reach maximun students or it was closed.")
                    
            else:
                room.student.remove(request.user)
            room.save()
            return redirect('home')
    user = request.user
    print(students)
    context = {
        'room':room,
        'func':func,
        'describetion':describetion,
        'students':students,
        'registable':not registable,
        'is_teacher':is_teacher,
        'user':user
    }
    return render(request, 'base/room.html',context)
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    courses = user.course_set.all()
    is_student = request.user.is_superuser
    context = {
        'courses':courses,
        'is_student':not is_student,
        'user':user

    }
    return render(request, 'base/userProfile.html', context)
def createCourse(request):
    if(request.user.is_superuser):
        form = CourseForm()
        if request.method == 'POST':
            # print(dict(request.POST)['student'])
            course = Course.objects.create(
            course_code = request.POST.get('course_code'),
            course_name = request.POST.get('course_name'),
            course_semeter = request.POST.get('course_semeter'),
            course_year = request.POST.get('course_year'),
            teacher = request.user,
            max_student = request.POST.get('max_student'),
            course_status = request.POST.get('course_status'),
            describetion = request.POST.get('describetion')
            )
            # course.student.set(request.POST)
            for i in dict(request.POST)['student']:
                course.student.add(i)
            course.save()
            
            return redirect('home')

            
        context = {
            'form':form,
        }
        return render(request, 'base/course_form.html',context)
    else:
        return redirect('home')
def editCourse(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)
    if request.user != course.teacher:
        return HttpResponse("You are not allowed to delete this course")
    if request.method == 'POST':
        course.course_code = request.POST.get('course_code')
        course.course_name = request.POST.get('course_name')
        course.course_semeter = request.POST.get('course_semeter')
        course.course_year = request.POST.get('course_year')
        course.teacher = request.user
        course.max_student = request.POST.get('max_student')
        course.course_status = request.POST.get('course_status')
        course.describetion = request.POST.get('describetion')
        # course.student.set(request.POST)
        course.student.clear()
        # print(dict(request.POST))
        if('student' in dict(request.POST).keys()):
            for i in dict(request.POST)['student']:
                course.student.add(i)
        course.save()
        return redirect('home')
    context = {
        'course':course,
        'form':form,
    }
    return render(request, 'base/edit_course.html', context)
def deleteCourse(request, pk):
    course = Course.objects.get(id=pk)
    if request.user != course.teacher:
        return HttpResponse("You are not allowed to delete this course")
    if request.method == 'POST':
        course.delete()
        return redirect('home')
    context = {
        'course':course,
    }
    return render(request,'base/delete_course.html',context)

    