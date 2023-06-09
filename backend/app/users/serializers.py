from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from titles.serializers import GenreSerializer, TitleSerializer

from users import models
from users.mixins.serializer_mixins import ExceptionParserMixin


class CreateUserSerializer(ExceptionParserMixin, serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'username',
            'email',
            'password',
        )

    def is_valid(self, raise_exception=False):
        try:
            super().is_valid(raise_exception=raise_exception)
        except ValidationError as exc:
            self._parse_exception(exc)
            raise exc


class HistorySerializer(serializers.ModelSerializer):
    titles = serializers.SerializerMethodField()

    class Meta:
        model = models.History
        fields = (
            'id',
            'date',
            'titles',
        )

    def get_titles(self, obj):
        titles = obj.title.all()
        serializer = TitleSerializer(titles, many=True)
        return serializer.data


class LikedTitleSerializer(TitleSerializer):
    pass


class DislikedTitleSerializer(TitleSerializer):
    pass


class PrefferedGenreSerializer(GenreSerializer):
    pass
