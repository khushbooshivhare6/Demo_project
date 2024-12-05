from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Message(models.Model):
    sender_email = models.EmailField()  # Email of the sender
    recipient_email = models.EmailField()  # Email of the recipient
    message = models.TextField()  # Content of the message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was created

    def __str__(self):
        return f"Message from {self.sender_email} to {self.recipient_email}"




class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to user model
    otp = models.CharField(max_length=6)  # OTP code
    created_at = models.DateTimeField(auto_now_add=True)  # Time when OTP was generated

    def is_valid(self):
        # OTP valid for 10 minutes (you can adjust this time)
        return (timezone.now() - self.created_at).seconds < 600

    def generate_otp(self):
        # Generate a random 6-digit OTP
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.save()

    def __str__(self):
        return f"OTP for {self.user.email}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    address = models.TextField()

    father_name = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=15, blank=True, null=True)

    mother_name = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
