from kanvas.permissions import IsInstructor
from accounts.serializers import UserSerializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError


class HandleGetAllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]
    name = "Accounts"

    def get(self, _) -> Response:
        users = User.objects.all()
        serializedUsers = UserSerializers(users, many=True).data
        return Response(serializedUsers, status=status.HTTP_200_OK)


class HandleLoginUser(APIView):
    def post(self, request) -> Response:
        try:
            username = request.data["username"]
            password = request.data["password"]

            is_user = authenticate(username=username, password=password)

            if is_user:
                token = Token.objects.get_or_create(user=is_user)[0].key
                return Response({"token": token}, status=status.HTTP_200_OK)

            return Response(
                {"error": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED
            )
        except KeyError:
            return Response(
                {"error": "Invalid keys."}, status=status.HTTP_406_NOT_ACCEPTABLE
            )


class HandleUser(APIView):
    def post(self, request):
        try:
            data = {
                "username": str(request.data["username"]),
                "password": str(request.data["password"]),
                "is_superuser": request.data["is_superuser"],
                "is_staff": request.data["is_staff"],
            }

            newUser = User.objects.create_user(**data)
            user = UserSerializers(newUser).data

            return Response(user, status=status.HTTP_201_CREATED)

        except KeyError:
            return Response(
                {"error": "Invalid keys."}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        except IntegrityError:
            return Response(
                {"error": "already registered user."}, status=status.HTTP_409_CONFLICT
            )
