from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog_post.models import Post
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.


def index(requests):
    posts = Post.objects.all()
    now = datetime.now()
    '''
    for count, post in enumerate(posts):
        # post_lists.append("#{}: {}<br><hr>".format(str(count), str(post)))
        post_lists.append("<h2>#{}: {} </h2><br><hr>".format(str(count), str(post)))
        post_lists.append("<small> {} </small><br><br>".format(str(post.content)))
    '''
    return render(requests, "pages/index.html", locals())


def showPost(requests, slug):
    now = datetime.now()
    try:
        post = Post.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return redirect('/')
    except MultipleObjectsReturned:
        return redirect('/')
    return render(requests, "pages/post.html", locals())
