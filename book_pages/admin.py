from django.contrib import admin
from .models import Book, Tag

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

# Register your models here.
admin.site.register(Book)
admin.site.register(Tag)
