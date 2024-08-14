from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Enrollment)

# odi mos sam interface za admin-a radit
# ako zatriba vidit ces
