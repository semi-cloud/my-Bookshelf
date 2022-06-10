from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/book/tag/{self.slug}/'


class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=10)
    content = models.CharField(max_length=500, blank=True)
    ratio = models.IntegerField(blank=True)

    image = models.ImageField(upload_to='book_pages/images/%Y/%m/%d/')     # 널 허용

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]'

    def get_absolute_url(self):
        return f'/book/{self.pk}/'

