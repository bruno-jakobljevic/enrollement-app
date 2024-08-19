from .models import Role
from django.shortcuts import redirect

def mentor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.role.role_name == Role.Roles.MENTOR:
                print("is mentor")
                return function(request, *args, **kwargs)
            else:
                return redirect('base')
        else:
            return redirect('login')
    return wrap

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.role.role_name == Role.Roles.ADMIN:
                return function(request, *args, **kwargs)
            else:
                return redirect('base')
        else:
            return redirect('login')
    return wrap


def student_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.role.role_name == Role.Roles.STUDENT:
                return function(request, *args, **kwargs)
            else:
                return redirect('base')
        else:
            return redirect('login')
    return wrap