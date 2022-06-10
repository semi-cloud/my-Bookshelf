import urllib
from urllib.parse import urlparse

import requests
from django.shortcuts import render

# Create your views here.

import json
from main import settings


def main(request):
    return render(
        request,
        'book/main.html',
    )


def add_book(request):
    if request.method == "POST":
        title = request.POST.get('item')
        print(title)
        return render(
            request,
            'book/main.html',
        )


def search(request):
    if request.method == 'GET':
        config_secret_debug = json.loads(open(settings.SECRET_DEBUG_FILE).read())
        rest_api_key = config_secret_debug['KAKAO']['REST_API_KEY']

        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        url = "https://dapi.kakao.com/v3/search/book?query=" + encText  # json 결과

        response = requests.get(urlparse(url).geturl(), headers={"Authorization": f'KakaoAK {rest_api_key}'}).json()
        print(response)
        json.dumps(response, indent=4, ensure_ascii=False)
        items = response.get('documents')

        context = {
            'items': items
        }
        return render(request, 'book/main.html', context=context)
