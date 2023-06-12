from titles import models


def get_titles():
    return models.Title.objects.all()[:10]
