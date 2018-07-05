#!/usr/bin/python
# -*- coding: utf8 -*-


import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django_filters import rest_framework as filters_rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import User, Post
from posts.serializers import UserSerializer, PostSerializer


def posts_number(queryset, name, value):
    return queryset.annotate(posts_num=Count('posts')).filter(posts_num__gte=value)


class UserFilter(filters_rest_framework.FilterSet):
    username = filters_rest_framework.CharFilter(name="username", lookup_expr="exact")
    posts_number = filters_rest_framework.Filter(name="posts_number", method=posts_number)

    class Meta:
        model = User
        fields = [
            'username',
            'posts_number'
        ]


class UserList(generics.ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter


class PostList(generics.ListAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class MyPostList(LoginRequiredMixin, generics.ListCreateAPIView):
    raise_exception = True
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user.pk)

    def post(self, request):
        data = json.loads(request.body)
        if 'title' not in data:
            return HttpResponseBadRequest('Title is not defined')

        if 'body' not in data:
            return HttpResponseBadRequest('Body is not defined')

        return super().post(request)


class MyPostDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    raise_exception = True

