from kanvas.permissions import IsInstructor
from kanvas.exceptions import BadRequestError, NotFoundError, OnlyThisError

from course.models import Course
from course.serializers import CourseSerializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import IntegrityError
from django.contrib.auth.models import User

# Create your views here.


class HandleCreateCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]
    name = "Handle course"

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

    def get(self, request) -> Response:
        courses = Course.objects.all()
        outputCourses = CourseSerializers(courses, many=True).data

        return Response(outputCourses, status=status.HTTP_200_OK)


class HandleCourseById(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]
    name = "Handle course"

    def put(self, request, course_id="") -> Response:
        try:
            foundCourse: Course = Course.objects.get(id=course_id)

            foundCourse.name = request.data["name"]
            foundCourse.save()

            course = CourseSerializers(foundCourse).data

            return Response(course, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response(
                {"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND
            )

        except IntegrityError:
            return Response(
                {"error": "Course with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, course_id) -> Response:
        try:
            course: Course = Course.objects.get(id=course_id)
            course.delete()

            return Response("", status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response(
                NotFoundError("Course").message, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, course_id) -> Response:
        try:
            course: Course = Course.objects.get(id=course_id)
            course = CourseSerializers(course).data

            return Response(course, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response(
                {"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND
            )


class HandleCourseUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]
    name = "Handle course users"

    def put(self, request, course_id="") -> Response:
        try:
            foundCourse: Course = Course.objects.get(id=course_id)
            foundCourse.users.set([])
            foundCourse.save()

            data: dict = dict(request.data)
            usersList = data["user_ids"]

            if type(usersList) != list:
                raise BadRequestError

            for id in usersList:
                user = User.objects.get(id=id)
                if user.is_staff == False and user.is_superuser == False:
                    foundCourse.users.add(id)
                else:
                    raise OnlyThisError("students")

            foundCourse.save()

            course = CourseSerializers(foundCourse).data
            return Response(course, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response(
                {"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"errors": "invalid user_id list"}, status=status.HTTP_404_NOT_FOUND
            )
        except KeyError:
            return Response(
                {"errors": "invalid user_id list"}, status=status.HTTP_404_NOT_FOUND
            )
        except OnlyThisError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        except BadRequestError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)
