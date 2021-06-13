from django.db import models
from datetime import date


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_DEFAULT,
        default=None,
    )
    body = models.TextField()
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        default=None
    )
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_DEFAULT,
        default=None,
    )
    body = models.TextField()
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.body
