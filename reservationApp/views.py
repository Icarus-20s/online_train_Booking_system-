from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from rest_framework.decorators import api_view
from .serializer import UserLoginSerializer, UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.


def homePage(request):
    return render(request, "home.html")


@api_view(["POST", "GET"])
def reservation(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return render(request, "register.html")
    serializer.save()
    return render(request, "login.html")


@api_view(["POST", "GET"])
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    print(request.__dict__)
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return HttpResponse("Invalid input!!")
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = User.objects.filter(email=email).first()
    if not user:
        return HttpResponse("user not found!!")

    if not check_password(password, user.password):
        return HttpResponse("Invalid credentials")
    token = RefreshToken.for_user(user)

    return HttpResponse(str(token))
