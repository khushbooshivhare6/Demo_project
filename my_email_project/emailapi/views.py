
from .models import Message,Teacher

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm
from .models import OTP
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import StudentForm,TeacherRegistrationForm
from django.views.decorators.csrf import csrf_exempt
from .models import Student

@csrf_exempt

def add_student(request):
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Send email
            send_mail(
                'Admission Successful',
                f'Hello {student.first_name},\n\nYour admission has been successfully submitted.',
                settings.EMAIL_HOST_USER,
                [student.email],
                fail_silently=False,
            )
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


@csrf_exempt
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'update_student.html', {'form': form})


@csrf_exempt
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'delete_student.html', {'student': student})


from django.http import HttpResponseForbidden

def student_list(request):
    

    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            # Save the teacher to the database
            teacher = form.save()

            # Send an email to the teacher after successful registration
            send_mail(
                'Teacher Registration Successful',
                f'Hello {teacher.first_name},\n\nYou have successfully registered as a teacher in the system.',
                settings.EMAIL_HOST_USER,  # The email address you want to send from
                [teacher.email],  # The email address to send the message to
                fail_silently=False,
            )

            # Redirect to the home page (or any other page as needed)
            return redirect('login')
    else:
        form = TeacherRegistrationForm()

    return render(request, 'teacher_register.html', {'form': form})

def send_otp_email(user_email, otp):
    subject = 'Your OTP Code for Registration'
    message = f'Your OTP code for registration is: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if password matches confirm password
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('register')

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect('register')

            # Create the user
            user = User.objects.create_user(email=email, password=password,username=username)

            # Generate OTP and send it to email
            otp_instance = OTP(user=user)
            otp_instance.generate_otp()
            send_otp_email(user.email, otp_instance.otp)

            # Redirect to OTP verification page
            request.session['user_id'] = user.id  # Store user ID in session for OTP verification
            return redirect('verify_otp')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import Teacher  # Assuming you have a Teacher model



@csrf_exempt
def verify_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

        # Check if email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect('verify_password')

        try:
            # Try to find the teacher by email
            teacher = Teacher.objects.get(email=email ,password=password)
            print("T:",teacher)

            
            if teacher.password==password:
                    
                    print(password)
                
                    messages.success(request, "Login successful!")
                    return redirect('student_list')  # Redirect to the student list or dashboard page
                
            else:
                messages.error(request, "Invalid password. Please try again.")
                return redirect('verify_password')

        except Teacher.DoesNotExist:
            # If the teacher with the given email doesn't exist
            messages.error(request, "Invalid email. Please try again.")
            return redirect('verify_password')

    return render(request, 'login.html')  # Return the password verification page


# @csrf_exempt
# def verify_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email, password)

#         # Check if both email and password are provided
#         if not email or not password:
#             messages.error(request, "Both email and password are required.")
#             return redirect('login')  # Redirect back to login page if fields are empty

#         try:
#             # Try to find the teacher by email
#             teacher = Teacher.objects.get(email=email)
#             print(teacher)

#             # Check if the password matches the stored hashed password
#             if teacher.check_password(password):
#                 # If the password is correct, log the teacher in
#                 auth_login(request, teacher)

#                 # Get the 'next' parameter (if any), or default to 'student_list' page
#                 next_url = request.GET.get('next', 'student_list')
#                 return redirect(next_url)  # Redirect to the appropriate page
#             else:
#                 messages.error(request, "Invalid email or password. Please try again.")
#                 return redirect('login')  # Redirect back to login page with error message
#         except Teacher.DoesNotExist:
#             messages.error(request, "Invalid email or password. Please try again.")
#             return redirect('login')  

#     return render(request, 'login.html')
    

from rest_framework.decorators import  permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login(request):
    return redirect('login')
   



def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, "Invalid session.")
            return redirect('register')

        try:
            user = User.objects.get(id=user_id)
            otp_instance = OTP.objects.get(user=user)

            if not otp_instance.is_valid():
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('register')

            if otp_instance.otp == otp_entered:
                user.is_active = True  # Activate the user
                user.save()

                login(request, user)  # Log the user in
                messages.success(request, "Registration successful!")
                return redirect('index')  # Redirect to home page or dashboard

            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('verify_otp')

        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP. Please request a new one.")
            return redirect('register')

    return render(request, 'verify_otp.html')


def index(request):
    if request.method == 'POST':
        message = request.POST['message']  # Get the message content
        sender_email = request.POST['email']  # Get the sender's email address
        # recipient_email = request.POST['emails']  # Get the recipient's email address

        subject = 'New Message from {}'.format(sender_email)  # Email subject

        # Send the email
        send_mail(
            subject,          # Subject of the email
            message,          # Message content
            settings.EMAIL_HOST_USER,  # Sender's email (from settings.py)
            # [recipient_email],          # Recipient's email address
            fail_silently=False
        )

        # Save the data in the database
        Message.objects.create(
            sender_email=sender_email,
            # recipient_email=recipient_email,
            message=message
        )

    return render(request, 'index.html')



# def index(request):
#     if request.method == 'POST':
#         message = request.POST['msg']
#         email = request.POST['email']
        
#         # Construct the subject and recipient list
#         subject = 'New Message from {}'.format(email)  # Customize subject if needed
#         recipient_list = [settings.EMAIL_HOST_USER]  # This is the email that will receive the message

#         
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,  # from_email
#             recipient_list,            # recipient_list
#             fail_silently=False
#         )
#     return render(request, 'index.html')

