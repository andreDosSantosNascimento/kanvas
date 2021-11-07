from accounts.permissions import IsInstructor, IsFacilitador, IsStudent
from accounts.serializers import UserSerializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsInstructor])
def get_all_users(_):
    users = User.objects.all()
    serializedUsers = UserSerializers(users, many=True).data
    return Response(serializedUsers, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    try:
        username = request.data["username"]
        password = request.data["password"]

        is_user = authenticate(username=username, password=password)

        if is_user:
            token = Token.objects.get_or_create(user=is_user)[0].key
            return Response({"token": token}, status=status.HTTP_200_OK)

        return Response({"error": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError:
        return Response(
            {"error": "Invalid keys"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )


@api_view(["POST"])
def create_user(request):
    try:
        data = {
            "username": str(request.data["username"]),
            "password": str(request.data["password"]),
            "is_superuser": bool(request.data["is_superuser"]),
            "is_staff": bool(request.data["is_staff"]),
        }

        newUser = User.objects.create_user(**data)
        user = UserSerializers(newUser).data

        return Response(user, status=status.HTTP_201_CREATED)
    except KeyError:
        return Response(
            {"error": "Invalid keys!"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
    except IntegrityError:
        return Response(
            {"error": "already registered user!"}, status=status.HTTP_409_CONFLICT
        )
