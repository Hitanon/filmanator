from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAuthenticated


class BasePreferencesMixin(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = None
    getter = None
    setter = None
    deleter = None

    @classmethod
    def action(cls, request, **kwargs):
        methods = {
            'GET': cls.getter,
            'POST': cls.setter,
            'DELETE': cls.deleter,
        }
        return methods[request.method](**kwargs)

    def get(self, request, *args, **kwargs):
        objects = self.action(request, **kwargs)
        serializer = self.serializer_class(objects, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.action(request, **kwargs)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        self.action(request, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
