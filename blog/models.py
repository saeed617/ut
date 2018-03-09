from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name='posts')
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name='comments')
    post = models.ForeignKey(Post, related_name='comments')
