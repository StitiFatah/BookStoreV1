from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = "books"

urlpatterns = [
    path("home/", views.home_display_books, name="display-books"),
    path("details/<uuid:book_id>/", views.DetailBook, name="detail-books"),
    path("create_book/", views.create_book, name="create-view"),
    path("update_book/<uuid:book_id>/",
         views.update_free_book, name="update-view"),
    path("create_non_free_book/",
         views.create_non_free_book, name="create-non-free-view"),
    path("update_non_free_book/<uuid:book_id>/",
         views.update_non_free_book, name="update-non-free-view"),
    path("delete_book/<uuid:pk>/", views.DeleteBook.as_view(), name="delete-view"),
    path("create_review/<uuid:book_id>/",
         views.CreateReview.as_view(), name="create-review"),
    path("update_review/<int:pk>/",
         views.UpdateReview.as_view(), name="update-review"),
    path("delete_review/<int:pk>/",
         views.DeleteReview.as_view(), name="delete-review"),
    path("search_nav/<str:requested_genre>/",
         views.search_nav, name="search-nav"),
    path('index_search/', views.IndexViews_search.as_view(), name="index-search"),
    path('index_specific_search/<str:requested_genre>/', views.IndexViews_specific_search.as_view(),
         name="index-specific-search"),


]
