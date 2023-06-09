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
        view_permissions = {
            'POST': [permissions.IsAnonymous()],
            'DELETE': [permissions.IsAuthenticated()],
        }
        return view_permissions[self.request.method]

    def post(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.create_user(**serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        self.check_permissions(request)
        services.delete_user(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.HistorySerializer

    def get(self, request, *args, **kwargs):
        histories = services.get_user_histories(request.user.id)
        serializer = self.serializer_class(histories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs):
        services.delete_user_history(id)
        return Response(status=status.HTTP_204_NO_CONTENT)



class LikedTitleView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.LikedTitleSerializer

    def get(self, request, *args, **kwargs):
        liked_titles = services.get_user_liked_titles(request.user.id)
        serializer = self.serializer_class(liked_titles, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, *args, **kwargs):
        services.add_user_liked_title(request.user.id, id)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id, *args, **kwargs):
        services.delete_user_liked_title(request.user.id, id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DislikedTitleView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.DislikedTitleSerializer

    def get(self, request, *args, **kwargs):
        disliked_titles = services.get_user_disliked_titles(request.user.id)
        serializer = self.serializer_class(disliked_titles, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, *args, **kwargs):
        services.add_user_disliked_title(request.user.id, id)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id, *args, **kwargs):
        services.delete_user_disliked_title(request.user.id, id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PreferredGenreView(APIView):
    pass


class DisfavoredGenreView(APIView):
    pass