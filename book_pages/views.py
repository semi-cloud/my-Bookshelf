from django.contrib.admin.views import main
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, ListView, DetailView
import urllib
from urllib.parse import urlparse

import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
# Create your views here.

import json

from .forms import BookForm, TagForm, CommentForm
from .models import Book, Tag, Follow, Comment
from main import settings


class BookUpdate(LoginRequiredMixin, UpdateView):  # create + update
    login_url = '/'
    model = Book
    form_class = BookForm
    template_name = "book_pages/book_form.html"

    def get_initial(self):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return {
            'title': book.title,
            'author': book.author,
            'image': book.image
        }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(BookUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class BookList(LoginRequiredMixin, ListView):  # 애초에 로그인 해야만 메인 페이지 접근 갸능
    login_url = '/'
    model = Book
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.method == "GET":
            name = self.request.GET.get('user')
            context = super(BookList, self).get_context_data()
            context['equals_user'] = True
            user = self.request.user
            if user.is_authenticated and (user.is_staff or user.is_superuser):
                if name:
                    user = get_user_by_name(name)
                    context['equals_user'] = False

            context['items'] = user.book_set.all()
            context['tag_list'] = user.tag_set.all()
            context['user'] = user
            context['neighbors'] = follow_list(self, user)
            return context


class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data()
        context['comment_form'] = CommentForm
        return context


class TagCreate(CreateView):
    model = Tag
    form_class = TagForm
    success_url = "/book/create/tag/"

    def get_context_data(self, **kwargs):
        context = super(TagCreate, self).get_context_data()
        context['tag_list'] = self.request.user.tag_set.all()
        return context

    # Post
    def form_valid(self, form):
        form.instance.slug = form.instance.name  # slug 값 채우기
        form.instance.user = self.request.user
        return super(TagCreate, self).form_valid(form)


def add_book(request):
    if request.method == "POST":
        # 검색 도서 DB에 먼저 저장
        book_pages = Book()
        item = request.POST.get('item')
        dict_item = json.loads(item.replace("'", "\""))
        book_pages.title = dict_item['title']
        book_pages.author = ','.join(dict_item['authors'])
        book_pages.image_url = dict_item['thumbnail']

        # 유저 저장
        current_user = request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            book_pages.user = current_user
        book_pages.save()
        return redirect(f'http://localhost:8000/book/create/{book_pages.pk}')


def tag_filter(request, slug):
    user = request.user
    tag = Tag.objects.get(slug=slug, user=user)
    book_list = tag.book_set.all()

    context = {
        'tag_list': user.tag_set.all(),
        'items': book_list,
        'neighbors': follow_list(None, user),
        'equals_user' : True
    }
    return render(request, 'book_pages/book_list.html', context)


def delete_book(request, pk):
    if request.user.is_authenticated:
        book = Book.objects.get(pk=pk)
        book.delete()
        return redirect("/book")
    else:
        raise PermissionDenied


def search(request):
    if request.method == 'GET':
        config_secret_debug = json.loads(open(settings.SECRET_DEBUG_FILE).read())
        rest_api_key = config_secret_debug['KAKAO']['REST_API_KEY']

        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        url = "https://dapi.kakao.com/v3/search/book?query=" + encText  # json 결과

        response = requests.get(urlparse(url).geturl(), headers={"Authorization": f'KakaoAK {rest_api_key}'}).json()
        json.dumps(response, indent=4, ensure_ascii=False)
        items = response.get('documents')

        context = {
            'items': items
        }
        return render(request, 'book_pages/search.html', context=context)


def follow_list(self, user):
    relation_list = Follow.objects.all()
    neighbor_list = []
    for relation in relation_list:
        if relation.follower == user:
            neighbor_list.append(relation.following)
    return neighbor_list


@csrf_exempt
def search_neighbor(request):
    if request.method == "GET":
        name = request.GET.get("username")
        user = get_user_by_name(name)
        if user:
            content = {"user": user.username, "email": user.email}
            return HttpResponse(json.dumps(content, indent=4, ensure_ascii=False))
        else:
            return HttpResponse("No matched User..Retry")


@csrf_exempt
def add_neighbor(request):
    if request.method == "GET":
        name = request.GET.get("user")
        relation = Follow()
        relation.follower = request.user
        relation.following = get_user_by_name(name)
        relation.save()
    return redirect("/book")


def add_comment(request, pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.book = book
                comment.user = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(book.get_absolute_url())
    else:
        raise PermissionDenied


def update_comment(request, book_pk, comment_pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=book_pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = Comment.objects.get(pk=comment_pk)
                comment.content = comment_form.instance.content
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(book.get_absolute_url())
    else:
        raise PermissionDenied


def delete_comment(request, book_pk, comment_pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=book_pk)

        if request.method == 'GET':
            comment = Comment.objects.get(pk=comment_pk)
            comment.delete()
            return redirect(book.get_absolute_url())
    else:
        raise PermissionDenied


def get_user_by_name(name):
    user = get_user_model().objects.get(username=name)
    if user:
        return user
    return None

