from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from kanvas.exceptions import BadRequestError
from kanvas.permissions import IsFacilitador, IsStudent

from django.contrib.auth.models import User
from django.db import IntegrityError

from activity.models import Activity, Submission
from activity.serializers import ActivitySerializer, SubmissionSerializer


class HandleActivities(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilitador]
    name = "Activity"

    def post(self, request) -> Response:
        try:
            data = {
                "title": request.data["title"],
                "points": request.data["points"],
            }
            activity = Activity.objects.create(**data)
            serializedActivity = ActivitySerializer(activity).data
            return Response(serializedActivity, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"error": "Activity with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request) -> Response:
        activities = Activity.objects.all()
        activitiesSerializers = ActivitySerializer(activities, many=True).data
        return Response(activitiesSerializers, status=status.HTTP_200_OK)


class HandleActivitiesById(APIView):
    def put(self, request, activity_id="") -> Response:
        try:
            data = request.data
            activity: Activity = Activity.objects.get(id=activity_id)
            have_submissions = Submission.objects.filter(activity_id=activity.id)

            if len(have_submissions) > 0:
                raise BadRequestError

            for key in data:
                if key == "title":
                    activity.title = data[key]
                elif key == "points":
                    activity.points = data[key]
                else:
                    raise BadRequestError("Bad request")
            activity.save()
            activity = ActivitySerializer(activity).data
            return Response(activity, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(
                {"error": "Activity with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except BadRequestError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)


class HandleSubmission(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStudent]
    name = "Submission"

    def post(self, request, activity_id="") -> Response:
        activity: Activity = Activity.objects.get(id=activity_id)

        data: dict = {
            "grade": None,
            "repo": request.data["repo"],
            "user_id": request.user.id,
            "activity_id": activity_id,
        }

        submission: Submission = Submission.objects.create(**data)

        activity.submissions.add(submission)

        submission = SubmissionSerializer(submission).data

        return Response(submission, status=status.HTTP_201_CREATED)


class HandleSubmissionById(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilitador]
    name = "Submission"

    def put(self, request, submission_id="") -> Response:
        submission: Submission = Submission.objects.get(id=submission_id)
        submission.grade = request.data["grade"]
        submission.save()
        submission = SubmissionSerializer(submission).data

        return Response(submission, status=status.HTTP_200_OK)


class HandleGetSubmissions(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request) -> Response:
        user: User = request.user

        submissions = []

        if user.is_staff or user.is_superuser:
            submissions: Submission = Submission.objects.all()
        else:
            submissions: Submission = Submission.objects.filter(user_id=user.id)

        submissions = SubmissionSerializer(submissions, many=True).data

        return Response(submissions, status=status.HTTP_200_OK)
