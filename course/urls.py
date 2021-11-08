from django.urls import path
from course.views import (
    HandleCourseById,
    HandleCourseUsers,
    HandleCreateCourse,
)

urlpatterns = [
    path("courses/", HandleCreateCourse.as_view()),
    path("courses/<int:course_id>/", HandleCourseById.as_view()),
    path("courses/<int:course_id>/registrations/", HandleCourseUsers.as_view()),
]
