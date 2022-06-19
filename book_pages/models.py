from urllib.request import urlopen

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import datetime


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'#{self.name}'

    def get_absolute_url(self):
        return f'/book/tag/{self.slug}/'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    content = models.CharField(max_length=500, blank=True)
    ratio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)

    image = models.ImageField(upload_to='book_pages/images/%Y/%m/%d/')
    image_url = models.URLField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.pk}'

    def get_absolute_url(self):
        return f'/book/{self.pk}/'

    def get_update_url(self):
        return f'/book/create/{self.pk}/'

    def get_delete_url(self):
        return f'/book/delete/{self.pk}/'

    def save(self, *args, **kwargs):       # 이미지 저장
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{datetime.datetime.now()}.jpg", File(img_temp))
        super(Book, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow_user")


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}:{self.content}'

    def get_absolute_url(self):
        return f'{self.book.get_absolute_url()}#comment-{self.pk}/'



