from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers, services, permissions


class UserView(APIView):

    def get_serializer_class(self):
        serializer_classes = {
            'POST': serializers.CreateUserSerializer,
        }
        return serializer_classes[self.request.method]

    def get_permissions(self):
        permission_classes = {
            'POST': permissions.NotAuthenticated(),
            'DELETE': permissions.IsAuthenticated(),
        }
        return [permission_classes[self.request.method]]

    def post(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_user(**serializer.data)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        self.check_permissions(request)
        services.delete_user(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
