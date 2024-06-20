from django.shortcuts import render
from .models import *
from django.http import Http404

def index(request):
    try:
        p = Profile.objects.all()
    except p.DoesNotExist:
        raise Http404("profiles do not exist")
    return render(request, "index.html", {"profiles": p})

