from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from reservationApp.models import User
from rest_framework.decorators import api_view, authentication_classes
from reservationApp.auth import UserAuthentication
from .serializer import UserLoginSerializer, UserSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
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
    print(User)
    print(password)

    if not check_password(password, user.password):
        return HttpResponse("Invalid credentials")

    token = RefreshToken.for_user(user)
    response = redirect("dashboard")
    response.set_cookie("token", str(token.access_token))
    return response


@authentication_classes([UserAuthentication])
def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"tickets": tickets})


@login_required
def book_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("dashboard")
    else:
        form = TicketForm()
    return render(request, "book_ticket.html", {"form": form})


@login_required
def cancel_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    if ticket:
        ticket.delete()
    return redirect("dashboard")
