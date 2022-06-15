from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='main'),
    path('<int:pk>/', views.BookDetail.as_view(), name="detail"),
    path('search/', views.search, name='search'),
    path('add/', views.add_book, name="add"),
    path('create/<int:pk>', views.BookUpdate.as_view()),
    path('create/tag/', views.TagCreate.as_view(), name="tag")
]
