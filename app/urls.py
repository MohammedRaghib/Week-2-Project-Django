from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/<str:tagname>', views.home, name='home'),
    path('home/', views.home, name='home_tagless'),
    path('logout/', views.logout_view, name='logout'),
    path('like/<int:picid>', views.like, name='like'),
    path('dislike/<int:picid>', views.dislike, name='dislike'),
    path('profile/', views.profile, name='profile'),
    path('editprof/', views.editprof, name='editprof'),
]