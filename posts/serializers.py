#!/usr/bin/python
# -*- coding: utf8 -*-


from rest_framework import serializers

from posts.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'registered_at', 'posts_number', 'posts_per_day')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body')

