from django.urls import path
from . import views

urlpatterns = [
    path("",views.homePage, name="home"),
    path("register/" , views.reservation ,name="register"),
    path("login/" , views.login ,name="login"),
]
