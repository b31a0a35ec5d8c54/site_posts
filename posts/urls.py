#!/usr/bin/python
# -*- coding: utf8 -*-


from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import UserList, PostList, MyPostList, MyPostDetail


urlpatterns = [
    url(r'^posts', PostList.as_view(), name='post_list'),
    url(r'^my_posts/$', MyPostList.as_view(), name='my_post_list'),
    url(r'^my_posts/(?P<pk>.+)/$', MyPostDetail.as_view(), name='my_post_detail'),
    url(r'^users/', UserList.as_view(), name='users'),

    url(r'^accounts/login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]

