from rest_framework import serializers

from users import exceptions, models


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
