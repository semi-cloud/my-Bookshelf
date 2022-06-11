from django import forms
from .models import Book, Tag


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'image', 'content', 'ratio', 'tags']


class TagForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Tag
        fields = ['name', 'slug']
        labels = {
            'name': 'Create Your Own Tag!'
        }