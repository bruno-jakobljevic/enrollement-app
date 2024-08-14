from django.contrib import admin
from django.urls import path
from enrollment import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="base"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('students/', views.students),
    path('courses/', views.courses)
]
