from django.shortcuts import render, redirect
import random
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User_class
from Home.views import Make_Homepage

subject_ = 'OTP for SignUp - '

def Login(request):
    if request.method == 'POST':
        if 'submit_btn' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(Make_Homepage)
            else:
                messages.error(request, 'Incorrect Password or Username')
                return render(request, "Login.html", {'messages': messages.get_messages(request)})
    else:
        if request.user.is_authenticated:
            return redirect(Make_Homepage)
        request.session.flush()
        return render(request, "Login.html")

def Set_Password(request):
    if '6' not in request.session:
        if '4' not in request.session:
            return redirect(Login)
        elif request.session['4'] == 1:
            return redirect(Reset_Password)
        else:
            return redirect(SignUp)
    
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 and password2 and password1 != password2:
            messages.error(request, "Passwords don't match")
            return render(request, "Set_Password.html", {'messages': messages.get_messages(request)})
        
        pattern = re.compile("(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}")
        valid = re.fullmatch(pattern, password1)
        if not valid:
            messages.error(request, "Please provide a stronger password as per the condition")
            return render(request, "Set_Password.html", {'messages': messages.get_messages(request)})

        username = request.session.get('1')
        designation = request.session.get('2')
        name = request.session.get('0')
        
        if request.session['4'] == 0:
            if not name or not username:
                messages.error(request, 'Missing user details. Please try again')
                return render(request, "Set_Password.html", {'messages': messages.get_messages(request)})
            
            user = User_class.objects.create_user(
                username=username, name=name, designation=designation, password=password2
            )
            request.session.flush()
            return redirect(Login)
        else:
            username = request.session['5']
            request.session.flush()
            user = User_class.objects.get(username=username)
            user.set_password(password2)
            user.save()
            return redirect(Login)
    
    return render(request, "Set_Password.html")

def Reset_Password(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        if not username:
            messages.error(request, "Please enter a username")
            return render(request, "Reset_Password.html", {'messages': messages.get_messages(request)})
        if not User_class.objects.filter(username=username).exists():
            messages.error(request, "No such username exists")
            return render(request, "Reset_Password.html", {'messages': messages.get_messages(request)})
        
        request.session['5'] = username
        request.session['4'] = 1
        global subject_
        subject_ = 'OTP for Reset Password - '
        return redirect(OTP_Send)
    
    return render(request, "Reset_Password.html")

def SignUp(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        designation = request.POST.get("designation")
        username = request.POST.get("username")

        if not all([name, designation, username]):
            messages.error(request, "All fields are required")
            return render(request, "SignUp.html", {'messages': messages.get_messages(request)})
        
        if "@" in username or "." in username or "iitk.ac.in" in username:
            messages.error(request, "Only username is needed, not the full email")
            return render(request, "SignUp.html", {'messages': messages.get_messages(request)})

        if User_class.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "SignUp.html", {'messages': messages.get_messages(request)})

        request.session['0'] = name
        request.session['1'] = username
        request.session['2'] = designation
        request.session['4'] = 0
        global subject_
        subject_ = 'OTP for SignUp - '
        return redirect(OTP_Send)
    
    options1 = not User_class.objects.filter(designation="Hall Manager").exists()
    return render(request, "SignUp.html", {"options1": options1})

def OTP_Send(request):
    if '6' not in request.session:
        otp = random.randint(100000, 999999)
        request.session['3'] = otp
        username = request.session.get('1') if request.session['4'] == 0 else request.session.get('5')
        
        user = User_class.objects.filter(username=username).first()  # Get user or None
        if user:
            name = user.name
        else:
            name = 'User'  # Default name if user is not found
        
        subject = f'{subject_} {otp}'
        message = f'Dear {name}, Your OTP is {otp}. Valid for 5 minutes. Do not share it.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f'{username}@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        return redirect(OTP)
    
    return redirect(Set_Password)


def OTP(request):
    if request.method == "POST":
        otp1 = request.POST.get("OTP")
        if not otp1:
            messages.error(request, "OTP field is empty")
            return render(request, "OTP.html", {'messages': messages.get_messages(request)})
        if str(request.session.get('3')) == otp1:
            request.session['6'] = 1
            return redirect(Set_Password)
        else:
            messages.error(request, 'Incorrect OTP')
            return render(request, "OTP.html", {'messages': messages.get_messages(request)})
    return render(request, "OTP.html")

def Logout(request):
    logout(request)
    return redirect(Login)
