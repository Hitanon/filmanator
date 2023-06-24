from questionnaire.exceptions import SessionNotFound

from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user.is_authenticated and user == obj.user):
            raise SessionNotFound()
        return True
