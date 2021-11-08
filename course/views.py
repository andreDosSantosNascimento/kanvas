from kanvas.permissions import IsInstructor
from kanvas.exceptions import NotFoundError

from course.models import Course
from course.serializers import CourseSerializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError

# Create your views here.


class HandleCreateCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]

    def post(self, request) -> Response:
        try:
            data = {"name": request.data["name"]}

            newCourse = Course.objects.create(**data)
            course = CourseSerializers(newCourse).data

            return Response(course, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"error": "Course with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class HandleCourseById(APIView):
    def put(self, request, course_id="") -> Response:
        try:
            foundCourse: Course = Course.objects.get(id=course_id)

            foundCourse.name = request.data["name"]
            foundCourse.save()

            course = CourseSerializers(foundCourse).data

            return Response(course, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response(
                NotFoundError("Course").message, status=status.HTTP_404_NOT_FOUND
            )

        except IntegrityError:
            return Response(
                {"error": "Course with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class HandleCourseUsers(APIView):
    def put(self, request, course_id="") -> Response:
        try:
            foundCourse = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                NotFoundError("Course").message, status=status.HTTP_404_NOT_FOUND
            )
