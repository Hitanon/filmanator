from users import exceptions, models, utils

from titles.models import Title


def create_user(**data):
    return models.User.objects.create_user(**data)


def delete_user(user_id):
    try:
        models.User.objects.get(id=user_id).delete()
    except models.User.DoesNotExist:
        raise exceptions.UserNotFound()


def get_user_histories(user_id):
    user = models.User.objects.get(id=user_id)
    histories = models.History.objects.filter(user=user)
    return histories


def group_histories_by_date(histories):
    histories_dict = utils.get_histories_dict(histories)
    return [models.GroupedHistory(date, histories_dict[date]) for date in histories_dict.keys()]


def delete_user_history(history_id):
    try:
        history = models.History.objects.get(id=history_id)
    except models.History.DoesNotExist:
        raise exceptions.UserNotFound()
    history.delete()


def get_user_liked_titles(user_id):
    user = models.User.objects.get(id=user_id)
    liked_title, _ = models.LikedTitle.objects.get_or_create(user=user)
    return liked_title.title.all()


def get_title(title_id):
    try:
        title = Title.objects.get(id=title_id)
    except Title.DoesNotExist:
        raise exceptions.UserNotFound()
    return title


def add_user_liked_title(user_id, title_id):
    title = get_title(title_id)
    user = models.User.objects.get(id=user_id)
    liked_title, _ = models.LikedTitle.objects.get_or_create(user=user)
    liked_title.title.add(title)


def delete_user_liked_title(user_id, title_id):
    title = get_title(title_id)
    user = models.User.objects.get(id=user_id)
    try:
        liked_title = models.LikedTitle.objects.get(user=user)
    except models.LikedTitle.DoesNotExist:
        raise exceptions.UserNotFound()
    liked_title.title.remove(title)


def get_user_disliked_titles(user_id):
    user = models.User.objects.get(id=user_id)
    disliked_title, _ = models.DislikedTitle.objects.get_or_create(user=user)
    return disliked_title.title.all()


def add_user_disliked_title(user_id, title_id):
    user = models.User.objects.get(id=user_id)
    title = get_title(title_id)
    disliked_title, _ = models.DislikedTitle.objects.get_or_create(user=user)
    disliked_title.title.add(title)


def delete_user_disliked_title(user_id, title_id):
    user = models.User.objects.get(id=user_id)
    title = get_title(title_id)
    disliked_title, _ = models.DislikedTitle.objects.get_or_create(user=user)
    disliked_title.title.remove(title)
