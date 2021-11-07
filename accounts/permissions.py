from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser


class IsFacilitador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser == False


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff == False and request.user.is_superuser == False
