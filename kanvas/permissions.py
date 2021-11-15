from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if view.name == "Course" and request.method == "GET":
            return True
        return request.user.is_staff and request.user.is_superuser


class IsFacilitador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            and request.user.is_superuser == False
            or request.user.is_staff
            and request.user.is_superuser
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if view.name == "Submission" and request.method == "GET":
            return True
        return request.user.is_staff == False and request.user.is_superuser == False
