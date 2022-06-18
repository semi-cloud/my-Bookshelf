from django import forms
from .models import Book, Tag, Comment


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
            'name': '커스텀 태그'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'cols': 100}),
        }

