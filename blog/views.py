from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.models import User
from . import models


def home(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = models.Post.objects.filter(user=user)
    return render(request, 'blog/profile.html', {'user': user, 'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    comments = models.Comment.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments':comments})