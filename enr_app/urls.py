from django.contrib import admin
from django.urls import path, include
from enrollment import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='base'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    path('students/', views.students, name='students'),
    path('add_student/', views.add_student, name='addstudent'),
    path('edit_student/<int:id>', views.edit_student, name='editstudent'),

    path('mentors/', views.mentors, name='mentors'),
    path('add_mentor/', views.add_mentor, name='addmentor'),
    path('edit_mentor/<int:id>', views.edit_mentor, name='editmentor'),

    path('courses/', views.courses, name='courses'),
    path('add_course/', views.add_course, name='addcourse'),
    path('edit_course/<int:id>', views.edit_course, name='editcourse'),
    path('add_mentor_to_course/<int:id>', views.add_mentor_to_course, name='addmentortocourse'),
    path('delete_course/<int:id>', views.delete_course, name='deletecourse'),
    path('confirm_delete/<int:id>', views.confirm_delete, name='confirmdelete'),
    path('courses/coursestudents/<int:id>', views.course_students, name='coursestudents'),
    
    path('enrollments/', views.enrollments, name='enrollments'),
    path('add_enroll/', views.add_enroll, name='addenroll'),
    path('edit_enroll/<int:id>', views.edit_enroll, name='editenroll'),

    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.SignUpView.as_view(), name='signup'),

    path("my_courses/", views.mentor_courses, name='mentor_courses'),
    path("my_courses/<int:id>/students", views.list_students_by_course, name="list_by_course"),
    path("my_courses/change_status/<int:id>", views.change_status_of_enrollment, name="changestatus")
]
