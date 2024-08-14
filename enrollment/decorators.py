from .models import Role
from django.shortcuts import redirect

def mentor_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.role_name == Role.MENTOR:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

def admin_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.role_name == Role.ADMIN:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

def student_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.role_name == Role.STUDENT:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap