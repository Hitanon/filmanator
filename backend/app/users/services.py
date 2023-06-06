from users import exceptions, models


def create_user(**data):
    return models.User.objects.create_user(**data)


def delete_user(user_id):
    try:
        user = models.User.objects.get(id=user_id)
        user.delete()
    except models.User.DoesNotExist:
        raise exceptions.UserNotFound
