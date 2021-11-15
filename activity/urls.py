from django.urls import path
from activity.views import (
    handleActivities,
    handleActivitiesById,
    handleGetSubmissions,
    handleSubmission,
    handleSubmissionById,
)

urlpatterns = [
    path("activities/", handleActivities.as_view()),
    path("activities/<int:activity_id>/", handleActivitiesById.as_view()),
    path("activities/<int:activity_id>/submissions/", handleSubmission.as_view()),
    path("submissions/<int:submission_id>/", handleSubmissionById.as_view()),
    path("submissions/", handleGetSubmissions.as_view()),
]
