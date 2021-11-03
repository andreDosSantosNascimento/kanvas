from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import views, response, status

from accounts.serializers import UserSerializers

# Create your views here.


class AccountsView(views.APIView):
    def get(self, request):
        users = User.objects.all()
        serializedUsers = UserSerializers(users, many=True).data
        return response.Response(serializedUsers, status=status.HTTP_200_OK)
