from django.shortcuts import render, get_object_or_404

from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView


from .models import *
from .decorators import *
from .forms import CourseForm, StudentForm, MentorCourseForm, StudentFormEdit, EnrollmentForm, CustomUserCreationForm, EditEnrollmentForm


def index(request):
    try:
        p = Profile.objects.all()
    except p.DoesNotExist:
        raise Http404("profiles do not exist")
    return render(request, 'base.html', {"profiles": p})

def students(request):
    try:
        p = Profile.objects.filter(role=3)
    except p.DoesNotExist:
        raise Http404("Profiles do not exist")
    return render(request, "students/students.html", {"data": p})

def add_student(request):

    if request.method == 'GET':
        form = StudentForm()
        return render(request, 'students/add_student.html', {"form":form})
    elif request.method == 'POST':        
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            return redirect('students')
        else:
            return render(request, 'students/add_student.html', {"form": form})
    else:
        return HttpResponseNotAllowed()

def edit_student(request, id):
    student = Profile.objects.get(pk=id)
    if request.method == 'GET':
        form = StudentFormEdit(instance=student)
        return render(request, 'students/edit_student.html', {"form":form})
    elif request.method == 'POST':
        form = StudentFormEdit(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
        else:
            return HttpResponseNotAllowed()
        
def mentors(request):
    try:
        mentors = Profile.objects.filter(role=2)
    except mentors.DoesNotExist:
        raise Http404("Mentors do not exist")
    return render(request, "mentors/mentors.html", {"data": mentors})

def add_mentor(request):
    if request.method == 'GET':
        form = StudentForm()
        return render(request, 'mentors/add_mentor.html', {"form":form})
    elif request.method == 'POST':        
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            return redirect('mentors')
        else:
            return render(request, 'mentors/add_mentor.html', {"form": form})
    else:
        return HttpResponseNotAllowed()

def edit_mentor(request, id):
    mentor = Profile.objects.get(pk=id)
    if request.method == 'GET':
        form = StudentFormEdit(instance=mentor)
        return render(request, 'mentors/edit_mentor.html', {"form":form})
    elif request.method == 'POST':
        form = StudentFormEdit(request.POST, instance=mentor)
        if form.is_valid():
            form.save()
            return redirect('mentors')
        else:
            return HttpResponseNotAllowed()

def courses(request):
    try:
        courses = Course.objects.all()
    except courses.DoesNotExist:
        raise Http404("Courses do not exist")
    return render(request, "courses/courses.html", {"data": courses})



def add_course(request):
    if request.method == 'GET':
        form = CourseForm()
        return render(request, 'courses/add_course.html', {"form":form})
    elif request.method == 'POST':        
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            return redirect('courses')
        else:
            return render(request, 'courses/add_course.html', {"form": form})
    else:
        return HttpResponseNotAllowed()
    
def edit_course(request, id):
    course = Course.objects.get(pk=id)
    if request.method == 'GET':
        form = CourseForm(instance=course)
        return render(request, 'courses/edit_course.html', {"form":form})
    elif request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            return HttpResponseNotAllowed()
        
def add_mentor_to_course(request, id):
    course = Course.objects.get(pk=id)
    if request.method == 'GET':
        form = MentorCourseForm(instance=course)
        return render(request, 'courses/edit_course.html', {"form":form})
    elif request.method == 'POST':
        form = MentorCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            return HttpResponseNotAllowed()
    
def delete_course(request, id):
    course = Course.objects.get(pk=id)
    if 'y' in request.POST:
        course.delete()
        return redirect('courses')
    else:
        return redirect('courses')

def confirm_delete(request, id):
    if request.method == 'GET':
        return render(request, 'courses/confirm_delete.html', {"data":id})
    else:
        return HttpResponseNotAllowed()
    
def course_students(request, id):
    course = get_object_or_404(Course, id=id)
    enrollments = Enrollment.objects.filter(course=course)
    students = [enrollment.student for enrollment in enrollments]
    return render(request, 'courses/course_enrollments.html', {
        'course': course,
        'students': students,
        'enrollments': enrollments,
    })

def enrollments(request):
    try:
        e = Enrollment.objects.all()
    except e.DoesNotExist:
        raise Http404("Profiles do not exist")
    return render(request, "enrollments/enrollments.html", {"data": e})

def add_enroll(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base') 
    else:
        form = EnrollmentForm()

    return render(request, 'enrollments/add_enroll.html', {'form': form})

def edit_enroll(request, id):
    enr = Enrollment.objects.get(pk=id)
    if request.method == 'GET':
        form = EnrollmentForm(instance=enr)
        return render(request, 'enrollments/edit_enroll.html', {"form":form})
    elif request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enr)
        if form.is_valid():
            form.save()
            return redirect('enrollments')
        else:
            return HttpResponseNotAllowed()

@mentor_required
def mentor_courses(request):
    try:
        mentor = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Mentor does not exist")
    
    if mentor.role.role_name == Role.Roles.MENTOR:
        courses = Course.objects.filter(course_mentor=mentor)
    else:
        courses = []
    
    return render(request, 'mentor_panel/mentor_courses.html', {'courses': courses})

@mentor_required
def list_students_by_course(request, id):
    try:
        course = Course.objects.get(pk=id)
        enrollments = Enrollment.objects.filter(course=course)
        status_filter = request.GET.get('status', None)
        if status_filter:
            enrollments = enrollments.filter(status=status_filter)
    except:
        raise Http404("Course does not exist")

    context = {
        'course': course,
        'enrollments': enrollments,
        'status_choices': Enrollment.Status.choices,
        'current_status': status_filter
    }

    return render(request, 'mentor_panel/students_by_course.html', context)

@mentor_required
def change_status_of_enrollment(request, id):
    enr = Enrollment.objects.get(pk=id)
    mentor = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        form = EditEnrollmentForm(instance=enr)
        return render(request, 'mentor_panel/change_status.html', {"form":form})
    elif request.method == 'POST':
        form = EditEnrollmentForm(request.POST, instance=enr)
        if form.is_valid():
            form.save()
            return redirect('mentor_courses')
        else:
            return HttpResponseNotAllowed()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'