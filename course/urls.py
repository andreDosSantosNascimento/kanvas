from django.urls import path
from course.views import HandleCourseById, HandleCreateCourse

urlpatterns = [
    path("courses/", HandleCreateCourse.as_view()),
    path("courses/<int:course_id>/", HandleCourseById.as_view()),
    path("courses/<int:course_id>/registrations/", HandleCreateCourse.as_view()),
]
