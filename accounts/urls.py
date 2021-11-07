from django.urls import path

from accounts.views import HandleGetAllUsers, HandleLoginUser, create_user

urlpatterns = [
    path("accounts/", create_user),
    path("users/", HandleGetAllUsers.as_view()),
    path("login/", HandleLoginUser.as_view()),
]
