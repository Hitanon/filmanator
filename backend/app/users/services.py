from titles.models import Title

from users import exceptions, models


def get_title(title_id):
    try:
        title = Title.objects.get(id=title_id)
    except Title.DoesNotExist:
        raise exceptions.TitleNotFound()
    return title


def get_genre(genre_id):
    try:
        genre = models.Genre.objects.get(id=genre_id)
    except models.Genre.DoesNotExist:
        raise exceptions.GenreNotFound()
    return genre


def get_user(user_id):
    try:
        return models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return None


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


def get_histories(user: models.User):
    try:
        return models.History.objects.get(user=user)
    except models.History.DoesNotExist:
        return None


def delete_user_history(user_id, history_id):
    try:
        get_user_histories(user_id).get(id=history_id).delete()
    except models.History.DoesNotExist:
        raise exceptions.HistoryNotFound()


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
        raise exceptions.TitleNotFound()
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
    preffered_genre, _ = models.PreferredGenre.objects.get_or_create(user=user)
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


def check_genre_id(**kwargs):
    genre_id = kwargs.get('genre', None)
    if genre_id is None:
        raise exceptions.GenreIdNotFound()
    return int(genre_id[0])


def check_title_id(**kwargs):
    title_id = kwargs.get('title', None)
    if title_id is None:
        raise exceptions.TitleIdNotFound()
    return int(title_id[0])
