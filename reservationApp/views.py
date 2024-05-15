from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
import requests


# Create your views here.

def homePage(request):
    return render(request , 'home.html')

def reservation(request):
    if request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request ,"Email already used")
            elif User.objects.filter(username=username).exists():
                messages.info(request , "Username already used")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username , email=email , password=password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request ,"password not same")
            return redirect ('register')
    return render(request , 'register.html')

def login(request):
    return render(request , 'login.html')



