import unittest
import json

from django.test import TestCase

from posts.models import User, Post
from posts.serializers import UserSerializer, PostSerializer


class UsersTest(TestCase):
    fixtures = ['testing']
    
    def setUp(self):
        self.john = User.objects.get(username='johndoe')
        self.jane = User.objects.get(username='janedoe')

    def test_users_get(self):
        response = self.client.get('/posts/users/', follow=True)

        self.assertEquals({user['username'] for user in response.json()}, {'admin', 'johndoe', 'janedoe'})
        self.assertEquals({field for field in response.json()[0]}, {'id', 'username', 'registered_at', 'posts_number', 'posts_per_day'})

    def test_users_post(self):
        data = {"username": "new_user"}

        response = self.client.post('/posts/users/', follow=True, data=json.dumps(data), content_type="application/json")
        
        self.assertEquals(response.status_code, 405)

    def test_users_get_filter_username(self):
        response = self.client.get('/posts/users/?username=johndoe', follow=True)

        self.assertEquals({user['username'] for user in response.json()}, {'johndoe'})
        self.assertJSONEqual(response.content, [UserSerializer(self.john).data])

    def test_users_get_filter_posts_number(self):
        response = self.client.get('/posts/users/?posts_number=3', follow=True)

        self.assertEquals({user['username'] for user in response.json()}, {'janedoe'})
        self.assertJSONEqual(response.content, [UserSerializer(self.jane).data])

    
class PostsTest(TestCase):
    fixtures = ['testing']
    
    def setUp(self):
        self.john = User.objects.get(username='johndoe')
        self.jane = User.objects.get(username='janedoe')
        self.post_data = {"title": "john doe third post", "body": "third body", "user": None}

    def test_posts_get(self):
        response = self.client.get('/posts/posts', follow=True)

        self.assertContains(response, 'john doe first post')
        self.assertContains(response, 'jane doe first post')

    def test_my_posts_not_authenticated(self):
        response = self.client.get('/posts/my_posts', follow=True)

        self.assertNotContains(response, 'john doe first post', status_code=403)
        self.assertNotContains(response, 'jane doe first post', status_code=403)

    def test_my_posts_get(self):
        login = self.client.login(username='johndoe', password='12345678')

        response = self.client.get('/posts/my_posts', follow=True)

        self.assertContains(response, 'john doe first post')
        self.assertNotContains(response, 'jane doe first post')

    def test_my_posts_post_without_title(self):
        login = self.client.login(username='johndoe', password='12345678')
        del self.post_data['title']

        response = self.client.post('/posts/my_posts/', data=json.dumps(self.post_data), content_type='application/json')

        self.assertContains(response, 'Title is not defined', status_code=400)

    def test_my_posts_post(self):
        self.assertEquals(self.john.my_posts.count(), 2)
        login = self.client.login(username='johndoe', password='12345678')
        self.post_data.update({'title': 'john doe third post', 'user': self.john.pk})

        response = self.client.post('/posts/my_posts/', data=json.dumps(self.post_data), content_type='application/json')

        self.assertContains(response, self.post_data['title'], status_code=201)
        self.assertEquals(self.john.my_posts.count(), 3)

    def test_my_post_put_not_authenticated(self):
        first = self.john.get_my_posts('first').get()
        new_title = 'john doe updated post'

        response = self.client.put('/posts/my_posts/{id}/'.format(id=first.id), data=json.dumps(self.post_data), content_type="application/json")

        self.assertEquals(response.status_code, 403)
        self.assertNotContains(response, new_title, 403)

    def test_my_post_put_not_existing(self):
        login = self.client.login(username='johndoe', password='12345678')
        new_title = 'john doe updated post'
        data = {"title": new_title, "body": '', "user": self.john.pk}

        response = self.client.put('/posts/my_posts/{id}/'.format(id=-1), data=json.dumps(data), content_type="application/json")

        self.assertEquals(response.status_code, 404)
        self.assertNotContains(response, new_title, 404)

    def test_my_post_put(self):
        login = self.client.login(username='johndoe', password='12345678')
        first = self.john.get_my_posts('first').get()
        self.post_data['user'] = self.john.pk

        response = self.client.put('/posts/my_posts/{id}/'.format(id=first.id), data=json.dumps(self.post_data), content_type="application/json")

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.post_data['title'])

    def test_my_post_delete(self):
        login = self.client.login(username='johndoe', password='12345678')
        first = self.john.get_my_posts('first').first()

        response = self.client.delete('/posts/my_posts/{id}/'.format(id=first.id))

        self.assertEquals(response.status_code, 204)

