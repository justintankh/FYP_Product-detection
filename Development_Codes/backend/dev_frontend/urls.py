from django.urls import path
from django.shortcuts import render


def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')


urlpatterns = [
    path('', index),
    path('signup', index),
    path('login', index),
    path('basket/<str:username>', index),
]
