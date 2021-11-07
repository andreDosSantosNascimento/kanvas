from django.urls import path

from accounts.views import create_user, get_all_users, login

urlpatterns = [
    path("accounts/", create_user),
    path("users/", get_all_users),
    path("login/", login),
]
