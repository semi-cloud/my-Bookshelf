from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='main'),
    path('<int:pk>/', views.BookDetail.as_view(), name="detail"),
    path('<int:pk>/comment/', views.add_comment),
    path('<int:book_pk>/update_comment/<int:comment_pk>/', views.update_comment),
    path('<int:book_pk>/delete_comment/<int:comment_pk>/', views.delete_comment),
    path('create/<int:pk>/', views.BookUpdate.as_view()),
    path('delete/<int:pk>/', views.delete_book),
    path('tag/<str:slug>/', views.tag_filter),
    path('tag/create', views.TagCreate.as_view(), name="tag_create"),
    path('tag/<str:slug>/delete/', views.delete_tag, name="tag_delete"),
    path('neighbor/add/', views.add_neighbor, name="follow"),
    path('neighbor/search/', views.search_neighbor, name="search_user"),
    path('search/', views.search, name='search'),
    path('add/', views.add_book, name="add"),
]
