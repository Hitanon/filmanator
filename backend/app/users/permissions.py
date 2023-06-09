from rest_framework.permissions import BasePermission

from users import exceptions


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise exceptions.AlreadyAuthorized()
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise exceptions.UserNotFound()
        return True
