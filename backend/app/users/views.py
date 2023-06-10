from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users import permissions, serializers, services
from users.mixins.view_mixins import BasePreferencesMixin


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
        return Response(status=status.HTTP_201_CREATED)

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

    def delete(self, request, history_id, *args, **kwargs):
        services.delete_user_history(history_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikedTitleView(BasePreferencesMixin):
    serializer_class = serializers.LikedTitleSerializer
    getter = services.get_user_liked_titles
    setter = services.add_user_liked_title
    deleter = services.delete_user_liked_title

    def get(self, request, *args, **kwargs):
        return super().get(request, user_id=request.user.id)

    def post(self, request, title_id, *args, **kwargs):
        return super().post(request, user_id=request.user.id, title_id=title_id)

    def delete(self, request, title_id, *args, **kwargs):
        return super().delete(request, user_id=request.user.id, title_id=title_id)


class DislikedTitleView(BasePreferencesMixin):
    serializer_class = serializers.DislikedTitleSerializer
    getter = services.get_user_disliked_titles
    setter = services.add_user_disliked_title
    deleter = services.delete_user_disliked_title

    def get(self, request, *args, **kwargs):
        return super().get(request, user_id=request.user.id)

    def post(self, request, title_id, *args, **kwargs):
        return super().post(request, user_id=request.user.id, title_id=title_id)

    def delete(self, request, title_id, *args, **kwargs):
        return super().delete(request, user_id=request.user.id, title_id=title_id)


class PreferredGenreView(BasePreferencesMixin):
    serializer_class = serializers.PrefferedGenreSerializer
    getter = services.get_preffered_genre
    setter = services.add_preffered_genre
    deleter = services.delete_preffered_genre

    def get(self, request, *args, **kwargs):
        return super().get(request, user_id=request.user.id)

    def post(self, request, genre_id, *args, **kwargs):
        return super().post(request, user_id=request.user.id, genre_id=genre_id)

    def delete(self, request, genre_id, *args, **kwargs):
        return super().delete(request, user_id=request.user.id, genre_id=genre_id)
