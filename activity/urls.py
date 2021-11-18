from django.urls import path
from activity.views import (
    HandleActivities,
    HandleActivitiesById,
    HandleGetSubmissions,
    HandleSubmission,
    HandleSubmissionById,
)

urlpatterns = [
    path("activities/", HandleActivities.as_view()),
    path("activities/<int:activity_id>/", HandleActivitiesById.as_view()),
    path("activities/<int:activity_id>/submissions/", HandleSubmission.as_view()),
    path("submissions/<int:submission_id>/", HandleSubmissionById.as_view()),
    path("submissions/", HandleGetSubmissions.as_view()),
]
