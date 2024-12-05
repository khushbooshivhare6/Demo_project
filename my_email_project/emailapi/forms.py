from django import forms
from .models import Student

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)  # Add username field
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'address', 
                  'father_name', 'father_mobile', 'mother_name', 'mother_mobile']

from .models import Teacher

class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'password']

class TeacherRegistrationForm1(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['email', 'password']        
