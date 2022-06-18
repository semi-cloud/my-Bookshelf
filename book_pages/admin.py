from django.contrib import admin
from .models import Book, Tag, Comment, Follow


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Follow)
