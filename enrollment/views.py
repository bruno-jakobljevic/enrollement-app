from django.shortcuts import render

from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout

from .models import *
from .decorators import *

def index(request):
    try:
        p = Profile.objects.all()
    except p.DoesNotExist:
        raise Http404("profiles do not exist")
    return render(request, "base.html", {"profiles": p})

def students(request):
    try:
        p = Profile.objects.all()
    except p.DoesNotExist:
        raise Http404("profiles do not exist")
    return render(request, "students.html", {"data": p})

def courses(request):
    try:
        s = Subject.objects.all()
    except s.DoesNotExist:
        raise Http404("subjects do not exist")
    return render(request, "courses.html", {"data": s})

def user_logout(request):
    logout(request)
    return render(request, 'logout.html', {})