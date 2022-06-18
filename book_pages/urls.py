from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='main'),
    path('<int:pk>/', views.BookDetail.as_view(), name="detail"),
    path('<int:pk>/comment/', views.add_comment),
    path('<int:book_pk>/update_comment/<int:comment_pk>/', views.update_comment),
    path('<int:book_pk>/delete_comment/<int:comment_pk>/', views.delete_comment),
    path('search/', views.search, name='search'),
    path('add/', views.add_book, name="add"),
    path('create/<int:pk>/', views.BookUpdate.as_view()),
    path('delete/<int:pk>/', views.delete_book),
    path('tag/<str:slug>/', views.tag_filter),
    path('create/tag/', views.TagCreate.as_view(), name="tag"),
    path('neighbor/add/', views.add_neighbor, name="follow"),
    path('neighbor/search/', views.search_neighbor, name="search_user"),
]
