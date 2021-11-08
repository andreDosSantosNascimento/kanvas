from django.urls import path

from accounts.views import HandleGetAllUsers, HandleLoginUser, HandleUser

urlpatterns = [
    path("accounts/", HandleUser.as_view()),
    path("users/", HandleGetAllUsers.as_view()),
    path("login/", HandleLoginUser.as_view()),
]
