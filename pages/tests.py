from django.test import TestCase
from django.urls import reverse, resolve


# class test_pages(TestCase):

#     def setUp(self):
#         self.response = self.client.get(reverse("pages:Home"))
#         self.response_1 = self.client.get(reverse("home"))

#     def test_home_page_status(self):
#         self.assertEqual(self.response.status_code, 200)

# also testing the home page from Bookstore original urls.py

# self.assertEqual(self.response_1.status_code, 200)

# def test_homepage_template(self):
#     self.assertTemplateUsed(self.response, "pages/home.html")

# also testing the home page from Bookstore original urls.py

# self.assertTemplateUsed(self.response_1, "pages/home.html")

# def test_homepage_html(self):
#     self.assertContains(self.response, "Home")

# also testing the home page from Bookstore original urls.py

#     self.assertContains(self.response_1, "Home")

# def test_resolve(self):
#     view = resolve("/pages/home/")
#     self.assertEqual(view.func.__name__, "TemplateView")
#     self.assertEqual(view.url_name, "Home")
#     self.assertEqual(view.app_names, ["pages"])
