from django.contrib import admin
from django.urls import path, include
from enrollment import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='base'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('delete_user/<int:user_id>', views.delete_user, name='deleteuser'),

    path('students/', views.students, name='students'),
    path('students/add_student/', views.add_student, name='addstudent'),
    path('students/edit_student/<int:student_id>', views.edit_student, name='editstudent'),
    path('students/student_enrollments/<int:student_id>', views.student_enrollments, name='studentenrollments'),

    path('mentors/', views.mentors, name='mentors'),
    path('mentors/add_mentor/', views.add_mentor, name='addmentor'),
    path('mentors/edit_mentor/<int:mentor_id>', views.edit_mentor, name='editmentor'),

    path('courses/', views.courses, name='courses'),
    path('courses/add_course/', views.add_course, name='addcourse'),
    path('courses/edit_course/<int:course_id>', views.edit_course, name='editcourse'),
    path('courses/add_mentor_to_course/<int:course_id>', views.add_mentor_to_course, name='addmentortocourse'),
    path('courses/delete_course/<int:course_id>', views.delete_course, name='deletecourse'),
    path('courses/coursestudents/<int:course_id>', views.course_students, name='coursestudents'),
    path('courses/enroll/<int:course_id>)', views.enroll, name="enroll"),
    path('courses/disenroll/<int:enrollment_id>', views.disenroll, name='disenroll'),
    path('courses/course_details/<int:course_id>', views.course_details, name='coursedetails'),
    
    path('enrollments/', views.enrollments, name='enrollments'),
    path('enrollments/add_enroll/', views.add_enroll, name='addenroll'),
    path('enrollments/edit_enroll/<int:enrollment_id>', views.edit_enroll, name='editenroll'),
    path('enrollments/delete_enroll/<int:enrollment_id>', views.delete_enroll, name='deleteenroll'),

    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name='signup'),

    path("my_courses/", views.mentor_courses, name='mentor_courses'),
    path("my_courses/<int:course_id>/students", views.list_students_by_course, name="listbycourse"),
    path("my_courses/change_status/<int:enrollment_id>", views.change_status_of_enrollment, name="changestatus"),

    path("my_enrollments/", views.my_enrollments, name='myenrollments'),
]
