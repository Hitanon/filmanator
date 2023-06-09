from rest_framework import serializers

from users import exceptions, models

from titles.serializers import TitleSerializer


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'username',
            'email',
            'password',
        )

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        if not is_valid and raise_exception:
            raise exceptions.IncorrectUserData()
        return is_valid


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


# class LikedTitleSerializer(serializers.Serializer):
#     titles = serializers.SerializerMethodField()

#     class Meta:
#         fields = (
#             'titles',
#         )

#     def get_titles(self, obj):
#         titles = obj.title.all()
#         serializer = TitleSerializer(titles, many=True)
#         return serializer.data


class LikedTitleSerializer(TitleSerializer):
    pass


class DislikedTitleSerializer(TitleSerializer):
    pass