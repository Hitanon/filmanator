from rest_framework import serializers

from titles import models


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Title
        fields = (
            'id',
            'title',
            'year',
            'imdb_rating',
            'votes_count',
            'is_movie',
            'duration',
            'seasons_count',
            'short_description',
        )


class TitleOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Title
        fields = (
            'id',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = (
            'id',
            'title',
        )
