from django.views.generic import CreateView, UpdateView, ListView, DetailView
import urllib
from urllib.parse import urlparse

import requests
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

import json

from .forms import BookForm, TagForm
from .models import Book, Tag
from main import settings


class BookUpdate(UpdateView):        # create + update
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


class BookList(ListView):
    model = Book
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookList, self).get_context_data()
        context['items'] = Book.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context


class BookDetail(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data()
        return context


class TagCreate(CreateView):
    model = Tag
    form_class = TagForm
    success_url = "/book/create/tag/"

    def get_context_data(self, **kwargs):
        context = super(TagCreate, self).get_context_data()
        context['tag_list'] = Tag.objects.all()
        return context

    # Post
    def form_valid(self, form):
        form.instance.slug = form.instance.name     # slug 값 채우기
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
        book_pages.save()

        return redirect(f'http://localhost:8000/book/create/{book_pages.pk}')


def tag_filter(request, slug):
    tag = Tag.objects.get(slug=slug)
    book_list = tag.book_set.all()

    context = {
        'tag_list': Tag.objects.all(),
        'items': book_list
    }
    return render(request, 'book_pages/book_list.html', context)


def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('http://localhost:8000/book/')


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


