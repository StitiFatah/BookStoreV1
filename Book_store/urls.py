from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from . import views
from books import views as booksViews
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("", booksViews.home_display_books, name="home"),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("pages/", include("pages.urls")),
    path("books/", include("books.urls")),
    path("library/", include("library.urls"))

]

if settings.DEBUG:
    import debug_toolbar
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
