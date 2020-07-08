from . import views
from django.urls import path
from django.views.generic import TemplateView

app_name = "pages"

urlpatterns = [
    path("home/", TemplateView.as_view(
        template_name="pages/home.html"), name="Home")

]
