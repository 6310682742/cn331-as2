from pydoc import describe
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

# Create your views here.

def home(request):
    print(request.user)
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

    context = {
        'courses':courses,
        'roomStatus':roomStatus,
        'q':q,

    }
    print(roomStatus)
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
    print(room.student.all())
    if(request.user in room.student.all()):
        func = "unregist"
    else:
        func = "regist"
    
    if request.method == 'POST':
        if request.user not in room.student.all():
            print(room.max_student > len(room.student.all()))
            if room.course_status == True and room.max_student > len(room.student.all()):
                room.student.add(request.user)
            else:
                return HttpResponse("You can not register this couse because this couse reach maximun students or it was closed.")
                
        else:
            room.student.remove(request.user)
        room.save()
        return redirect('home')
    context = {
        'room':room,
        'func':func,
        'describetion':describetion
    }
    return render(request, 'base/room.html',context)
def userProfile(request):
    courses = Course.objects.filter(student=request.user)
    context = {
        'courses':courses
    }
    return render(request, 'base/userProfile.html', context)
