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
    path('index_filtering/<str:filtre>/', views.home_display_books_filtered,
         name="display-filtered"),
    path("cart/", views.Cart_display_view, name="user-cart"),
    path("add_to_cart/<uuid:book_id>/",
         views.add_item_to_cart, name="add-to-cart"),
    path("remove_from_cart/<uuid:book_id>/",
         views.remove_item_from_cart, name="remove-from-cart"),
    path("empty_cart/",
         views.empty_cart, name="empty-cart"),
    path("checkout/",
         views.checkout, name="checkout"),
    path("order/", views.create_order, name="create-order"),
    path("order_summary/", views.order_summary, name="order-summary"),
    path("charge/", views.charge, name="charge"),
    path("confirmed_orders/", views.display_ordered_books,
         name="confirmed-ordered-books"),
    path("settings/", views.Settings,
         name="settings"),






]
