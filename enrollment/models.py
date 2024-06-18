from django.db import models
from django.contrib.auth.models import User
# Create your models here.d

class Role(models.Model):
    class Roles(models.TextChoices):
        MENTOR = 'M', 'Mentor'
        STUDENT = 'S', 'Student'

    role_name = models.CharField(max_length=2, choices=Roles.choices, default=Roles.STUDENT)

class Profile(models.Model):
    class Status(models.TextChoices):
        NONE = 'N', 'None'
        FULL_TIME = 'FT', 'Full-time'
        PART_TIME = 'PT', 'Part-time'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.NONE)

class Subject(models.Model):
    class Electiveness(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    course_mentor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    credits = models.IntegerField()
    semester_full_time = models.IntegerField()
    semester_part_time = models.IntegerField()
    is_elective = models.CharField(max_length=2, choices=Electiveness.choices, default=Electiveness.NO)

class Enrollment(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    predmet = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=64)