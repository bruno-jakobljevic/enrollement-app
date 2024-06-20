from django.contrib import admin
from django.urls import include, path
from enrollment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
]
