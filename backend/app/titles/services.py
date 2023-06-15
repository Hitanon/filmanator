from titles import models


def get_titles_by_attrs():
    return models.Title.objects.all()[:10]
