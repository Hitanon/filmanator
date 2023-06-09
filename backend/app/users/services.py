from titles.models import Title

from users import exceptions, models


def get_title(title_id):
    try:
        title = Title.objects.get(id=title_id)
    except Title.DoesNotExist:
        raise exceptions.UserNotFound()
    return title


def get_genre(genre_id):
    try:
        genre = models.Genre.objects.get(id=genre_id)
    except models.Genre.DoesNotExist:
        raise exceptions.UserNotFound()
    return genre


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


def get_preffered_genre(user_id):
    user = models.User.objects.get(id=user_id)
    preffered_genre = models.PreferredGenre.objects.get_or_create(user=user)
    return preffered_genre.genre.all()


def add_preffered_genre(user_id, genre_id):
    user = models.User.objects.get(id=user_id)
    genre = get_genre(genre_id)
    preffered_genre, _ = models.PreferredGenre.objects.get_or_create(user=user)
    preffered_genre.genre.add(genre)


def delete_preffered_genre(user_id, genre_id):
    user = models.User.objects.get(id=user_id)
    genre = get_genre(genre_id)
    preffred_genre, _ = models.PreferredGenre.objects.get_or_create(user=user)
    preffred_genre.genre.remove(genre)


def get_disfavored_genre(user_id):
    user = models.User.objects.get(id=user_id)
    disfavored_genre, _ = models.DisfavoredGenre.objects.get_or_create(user=user)
    return disfavored_genre.genre.all()


def add_disfavored_genre(user_id, genre_id):
    user = models.User.objects.get(id=user_id)
    genre = get_genre(genre_id)
    disfavored_genre, _ = models.DisfavoredGenre.objects.get_or_create(user=user)
    disfavored_genre.genre.add(genre)


def delete_disfavored_genre(user_id, genre_id):
    user = models.User.objects.get(id=user_id)
    genre = get_genre(genre_id)
    disfavored_genre, _ = models.DisfavoredGenre.objects.get_or_create(user=user)
    disfavored_genre.genre.remove(genre)
