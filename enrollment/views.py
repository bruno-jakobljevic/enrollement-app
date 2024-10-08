from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponseNotAllowed, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .models import *
from .decorators import *
from .forms import CourseForm, StudentForm, MentorForm, MentorCourseForm, StudentFormEdit, EnrollmentForm, CustomUserCreationForm, EditEnrollmentForm


def index(request):
    try:
        profiles = Profile.objects.all()
    except Profile.DoesNotExist:
        profiles = []
    return render(request, 'base.html', {"profiles": profiles})

def courses(request):
    try:
        courses = Course.objects.all()
    except Course.DoesNotExist:
        courses = []
    return render(request, "courses/courses.html", {"data": courses})

@admin_required
def students(request):
    try:
        students = Profile.objects.filter(role=3)
    except Profile.DoesNotExist:
        students = []
    return render(request, "students/students.html", {"data": students})

@admin_required
def add_student(request):
    if request.method == 'GET':
        form = StudentForm()
        return render(request, 'students/add_student.html', {"form":form})
    elif request.method == 'POST':        
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
        else:
            messages.error(request, "Form is not valid")
            return redirect('students')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required
def edit_student(request, student_id):
    student = get_object_or_404(Profile, pk=student_id)
    if request.method == 'GET':
        form = StudentFormEdit(instance=student)
        return render(request, 'students/edit_student.html', {"form":form})
    elif request.method == 'POST':
        form = StudentFormEdit(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
        else:
            messages.error(request, "Form is not valid")
            return redirect('students')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required 
def mentors(request):
        try:
            mentors = Profile.objects.filter(role=2)
        except Profile.DoesNotExist:
            mentors = []
        return render(request, "mentors/mentors.html", {"data": mentors})

@admin_required
def add_mentor(request):
    if request.method == 'GET':
        form = MentorForm()
        return render(request, 'mentors/add_mentor.html', {"form":form})
    elif request.method == 'POST':        
        form = MentorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mentors')
        else:
            messages.error(request, "Form is not valid")
            return redirect('mentors')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required
def edit_mentor(request, mentor_id):
    mentor = get_object_or_404(Profile, pk=mentor_id)
    if request.method == 'GET':
        form = StudentFormEdit(instance=mentor)
        return render(request, 'mentors/edit_mentor.html', {"form":form})
    elif request.method == 'POST':
        form = StudentFormEdit(request.POST, instance=mentor)
        if form.is_valid():
            form.save()
            return redirect('mentors')
        else:
            messages.error(request, "Form is not valid")
            return redirect('mentors')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required
def add_course(request):
    if request.method == 'GET':
        form = CourseForm()
        return render(request, 'courses/add_course.html', {"form":form})
    elif request.method == 'POST':        
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            messages.error(request, "Form is not valid")
            return redirect('courses')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'GET':
        form = CourseForm(instance=course)
        return render(request, 'courses/edit_course.html', {"form":form})
    elif request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            messages.error(request, "Form is not valid")
            return redirect('mentors')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required
def add_mentor_to_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'GET':
        form = MentorCourseForm(instance=course)
        return render(request, 'courses/edit_course.html', {"form":form})
    elif request.method == 'POST':
        form = MentorCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Form is not valid")
            
        return redirect('courses')
    else:
        return HttpResponseNotAllowed('GET', 'POST')
    
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('base')  
    return render(request, 'confirm_delete.html')

@admin_required
def delete_enroll(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == "GET":
        return render(request, 'confirm_delete.html')
    elif request.method == "POST":
        enrollment.delete()
        messages.success(request, 'Enrollment deleted successfully')
        return redirect('base')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    
@admin_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        course.delete()
        messages.success(request, 'Course deleted successfully')
        return redirect('base')  
    return render(request, 'confirm_delete.html')

@admin_required
def course_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(course=course)

    return render(request, 'courses/course_enrollments.html', {
        'course': course,
        'enrollments': enrollments,
    })

@admin_required
def enrollments(request):
    try:
        ernollments = Enrollment.objects.all()
    except ernollments.DoesNotExist:
        raise Http404("Enrollments do not exist")
    return render(request, "enrollments/enrollments.html", {"data": ernollments})

@admin_required
def add_enroll(request):
    if request.method == 'GET':
        form = EnrollmentForm()
        return render(request, 'enrollments/add_enroll.html', {'form': form})
    elif request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']

            if Enrollment.objects.filter(student=student, course=course).exists():
                messages.error(request, 'This student is already enrolled in this course.')
                return redirect('enrollments')
            
            form.save()
            return redirect('enrollments')
        else:
            messages.error(request, 'Form is not valid')
            return redirect('base')
    else:
        HttpResponseNotAllowed('GET', 'POST')
    
@admin_required
def edit_enroll(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    if request.method == 'GET':
        form = EnrollmentForm(instance=enrollment)
        return render(request, 'enrollments/edit_enroll.html', {"form":form})
    elif request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Form is not valid')
    return redirect('enrollments')

@admin_required
def student_enrollments(request, student_id):
    profile = get_object_or_404(Profile, id=student_id)
    enrollments = Enrollment.objects.filter(student=profile)

    return render(request, 'students/student_enrollments.html', {'enrollments': enrollments, 'student': profile})

@mentor_required
def mentor_courses(request):
    mentor = get_object_or_404(Profile, user=request.user)
    try:
        courses = Course.objects.filter(course_mentor=mentor)
    except Course.DoesNotExist:
        courses = []
    
    return render(request, 'mentor_panel/mentor_courses.html', {'courses': courses})

@mentor_required
def list_students_by_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    status_filter = request.GET.get('status')

    if status_filter:
        enrollments = Enrollment.objects.filter(course=course, status=status_filter)

    context = {
        'course': course,
        'enrollments': enrollments,
        'status_choices': Enrollment.Status.choices,
        'current_status': status_filter
    }

    return render(request, 'mentor_panel/students_by_course.html', context)

@mentor_required
def change_status_of_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'GET':
        form = EditEnrollmentForm(instance=enrollment)
        return render(request, 'mentor_panel/change_status.html', {"form": form, "enrollment": enrollment})
    elif request.method == 'POST':
        form = EditEnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'Form is not valid')
        return redirect('mentor_courses')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    
@student_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile = get_object_or_404(Profile, user=request.user)

    if Enrollment.objects.filter(student=profile, course=course).exists():
        messages.error(request, 'You are already enrolled in this course.')
        return redirect('courses')
    
    enrollment = Enrollment(student=profile, course=course, status=Enrollment.Status.ENROLLED)
    enrollment.save()

    return redirect('myenrollments')

@student_required
def my_enrollments(request):
    profile = get_object_or_404(Profile, user=request.user)
    enrollments = Enrollment.objects.filter(student=profile)

    return render(request, 'student_panel/my_enrollments.html', {'enrollments': enrollments, 'student': profile})

@student_required
def disenroll(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student__user=request.user)
    enrollment.delete()
    return redirect('myenrollments')

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_details.html', {'course': course})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'