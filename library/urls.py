from django.urls import path
from . import views


app_name = "library"


urlpatterns = [
    path("main/", views.Library, name="main-library"),
    path("add_free_to_library/<uuid:book_id>/", views.add_free_book_to_library,
         name="add-free-to-library"),
    path("remove_form_library/<uuid:book_id>/", views.remove_free_book_from_library,
         name="remove-free-from-library"),



]
