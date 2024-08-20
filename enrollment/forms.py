from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Course, Profile, Role, User, Enrollment

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Course Name"
        self.fields['code'].label = "Course Code"
        self.fields['course_mentor'].label = "Mentor"
        self.fields['description'].label = "Course Description"
        self.fields['credits'].label = "ECTS"
        self.fields['semester_full_time'].label = "Full-Time Semester"
        self.fields['semester_part_time'].label = "Part-Time Semester"
        self.fields['is_optional'].label = "Optional"

        mentor_role = Role.objects.get(role_name=Role.Roles.MENTOR)
        self.fields['course_mentor'].queryset = Profile.objects.filter(role=mentor_role)

class MentorCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_mentor']

    def __init__(self, *args, **kwargs):
        super(MentorCourseForm, self).__init__(*args, **kwargs)
        mentor_role = Role.objects.get(role_name=Role.Roles.MENTOR)
        self.fields['course_mentor'].queryset = Profile.objects.filter(role=mentor_role)

class StudentForm(ModelForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    status = forms.ChoiceField(
        choices=[(value, label) for value, label in Profile.Status.choices if value != 'N'],
        required=True
    )

    class Meta:
        model = Profile
        fields = ['status']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        profile, created = Profile.objects.get_or_create(user=user)

        if created:
            profile.status = self.cleaned_data['status']
            profile.role = Role.objects.get(role_name=Role.Roles.STUDENT)
            if commit:
                profile.save()

        return profile
    
class MentorForm(ModelForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = []

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        profile, created = Profile.objects.get_or_create(user=user)

        if created:
            profile.status = Profile.Status.NONE
            profile.role = Role.objects.get(role_name=Role.Roles.STUDENT)
            if commit:
                profile.save()

        return profile

    
class StudentFormEdit(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Profile
        fields = ['role', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance').user if kwargs.get('instance') else None
        super(StudentFormEdit, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        user = None
        if self.instance and self.instance.user:
            user = self.instance.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
        else:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            self.instance.user = user

        profile = super(StudentFormEdit, self).save(commit=False)
        if commit:
            profile.save()
        return profile

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']

    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        student_role = Role.objects.get(role_name=Role.Roles.STUDENT)
        self.fields['student'].queryset = Profile.objects.filter(role=student_role)

class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']

    def __init__(self, *args, **kwargs):
        super(StudentEnrollmentForm, self).__init__(*args, **kwargs)
        student_role = Role.objects.get(role_name=Role.Roles.STUDENT)
        self.fields['student'].queryset = Profile.objects.filter(role=student_role)

class EditEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['status']

class MentorFormEdit(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Profile
        fields = ['role', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance').user if kwargs.get('instance') else None
        super(MentorFormEdit, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        user = None
        if self.instance and self.instance.user:
            user = self.instance.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
        else:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
            self.instance.user = user

        profile = super(MentorFormEdit, self).save(commit=False)
        if commit:
            profile.save()
        return profile
        
class CustomUserCreationForm(UserCreationForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.exclude(role_name=Role.Roles.ADMIN),
        label="Role"
    )
    status = forms.ChoiceField(
        choices=Profile.Status.choices,
        label="Status"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'status']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.role = self.cleaned_data['role']
                profile.status = self.cleaned_data['status']
                profile.save()
        return user