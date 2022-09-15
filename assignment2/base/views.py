import http
from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    context = {}
    return render(request, 'base/home.html', context)
def login(request):
    context = {}
    return render(request,'base/login.html',context)