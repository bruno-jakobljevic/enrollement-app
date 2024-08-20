from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'A', 'Admin'
        MENTOR = 'M', 'Mentor'
        STUDENT = 'S', 'Student'

    role_name = models.CharField(max_length=2, choices=Roles.choices)

    def __str__(self):
        return self.get_role_name_display()

class Profile(models.Model):
    class Status(models.TextChoices):
        NONE = 'N', 'None'
        FULL_TIME = 'FT', 'Full-time'
        PART_TIME = 'PT', 'Part-time'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True, default=3)
    status = models.CharField(max_length=2, choices=Status.choices, default='FT')

    def __str__(self):
        return self.user.username + " - " + self.role.__str__() + " - " + self.user.email + " - " + self.get_status_display()

class Course(models.Model):
    class Optional(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    course_mentor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    credits = models.IntegerField()
    semester_full_time = models.IntegerField()
    semester_part_time = models.IntegerField()
    is_optional = models.CharField(max_length=2, choices=Optional.choices, default=Optional.NO)
    def __str__(self):
        return self.name + " - " + str(self.code) + " - " + str(self.credits) + " ECTS"

class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = 'E', 'Enrolled'
        PASSED = 'P', 'Passed'
        FAILEDREQ = 'FR', 'Failed Requirements'

    student = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.ENROLLED)

    def __str__(self):
        return self.student.user.username + " - " + self.course.name + " - " + self.get_status_display() 