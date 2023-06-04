from config.settings import AUTH_USER_MODEL

from django.db import models


class Session(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    ends_at = models.DateTimeField()


class Category(models.Model):
    priority = models.IntegerField()


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Criterion(models.Model):
    title = models.CharField(unique=True)
    body = models.CharField()
    questions = models.ManyToManyField(Question)


class Answer(models.Model):
    body = models.CharField()
    questions = models.ManyToManyField(Question)


class Result(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
