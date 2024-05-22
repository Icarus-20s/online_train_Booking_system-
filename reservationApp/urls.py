from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("book/", views.book_ticket, name="book_ticket"),
    path("logout/", views.logout, name="logout"),
    path("cancel/<int:ticket_id>/", views.cancel_ticket, name="cancel_ticket"),
]
