from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from reservationApp.models import User
from rest_framework.decorators import api_view, authentication_classes
from reservationApp.auth import UserAuthentication
from .serializer import UserLoginSerializer, UserSerializer, TicketSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ticket, Train
from django.views.decorators.csrf import csrf_exempt


def homePage(request):
    return render(request, "home.html")


@api_view(["POST", "GET"])
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors)
    serializer.save()
    return render(request, "login.html")


@api_view(["POST", "GET"])
@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = User.objects.filter(email=email).first()

    if not user:
        return HttpResponse("User not found!!")

    if not check_password(password, user.password):
        return HttpResponse("Invalid credentials")

    token = RefreshToken.for_user(user)
    response = redirect("dashboard")
    response.set_cookie("token", str(token.access_token))
    return response


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user).all()
    user_booked_trains=Ticket.objects.filter(user=request.user).values_list('train_id', flat=True)
    available_trains = Train.objects.exclude(id__in=user_booked_trains).all()
    return render(request, "dashboard.html", {"tickets": tickets, "available_trains":available_trains})


@api_view(["POST", "GET"])
@authentication_classes([UserAuthentication])
def book_ticket(request):
    data = request.data.copy()
    data["user"]=request.user.id
    user_booked_trains=Ticket.objects.filter(user=request.user).values_list('train_id', flat=True)
    available_trains = Train.objects.exclude(id__in=user_booked_trains).all()
    if request.method == "GET":
        return render(request, "book_ticket.html", {"trains": available_trains})
    serializer = TicketSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors)
    serializer.save()
    response = redirect("dashboard")
    return response



@api_view(["GET"])
@authentication_classes([UserAuthentication])
def cancel_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    if ticket:
        ticket.delete()
    return redirect("dashboard")

@api_view(["POST", "GET"])
@authentication_classes([UserAuthentication])
def logout(request):
    response = redirect("login")
    response.delete_cookie("token")
    return response
