from venv import create
from django.urls import path
from .views import *


urlpatterns = [
    path('',homeView,name='home'),
    path('login/',loginView,name='login'),
    path('register/',registerView,name='register'),
    path('logout/',logoutView,name='logout'),
    path('createArticle/',createArticle,name='createArticle'),
    path('details/<str:pk>/',detailsView,name='details'),
    path('deleteArticle/<str:pk>/',deleteArticle,name='deleteArticle'),
    path('updateArticle/<str:pk>/',updateArticle,name='updateArticle'),
    path('deleteComment/<str:pk>/',deleteComment,name='deleteComment'),
    path('like/<str:pk>/',like,name='like'),
    path('dislike/<str:pk>/',dislike,name='dislike'),
    path('profile/',profile,name='profile')
]
