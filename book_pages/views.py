from django.views.generic import CreateView, UpdateView
import urllib
from urllib.parse import urlparse

import requests
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

import json

from .forms import BookForm
from .models import Book
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


def main(request):
    return render(
        request,
        'book_pages/main.html',
    )


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
        return render(request, 'book_pages/main.html', context=context)
