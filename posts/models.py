import datetime

from django.db import models
from django.contrib.auth.models import User as BaseUser


class User(BaseUser):

    class Meta:
        proxy = True

    def __str__(self):
        return '{}' .format(self.username)

    def get_my_posts(self, title=None):
        qs = Post.objects.filter(user=self)
        if title:
            qs = qs.filter(title__contains=title)
        return qs

    @property
    def my_posts(self):
        return self.get_my_posts()

    def registered_at(self):
        return str(self.date_joined)

    def posts_number(self):
        return self.get_my_posts().count()

    def posts_per_day(self):
        post_count = self.posts_number()
        now = datetime.datetime.now(datetime.timezone.utc)
        day_count = (now - self.date_joined).days
        if day_count == 0:
            return 0

        return post_count / day_count


class Post(models.Model):

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return '{}' .format(self.title)

    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=64)
    body = models.TextField()
