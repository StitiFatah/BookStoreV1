from django.test import TestCase
from django.urls import reverse, resolve
from books.models import Books
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime


def create_user(username, email):
    return get_user_model().objects.create_user(
        username=username, email=email, date_of_birth="1992-10-02", password="testing1234")


def create_books(title, pub_date, user, price=0):

    return Books(title=title, pub_date=pub_date,
                 original_poster=user, price=price).save()


class TestHomeDisplayBooks(TestCase):
    # def setUp(self):
    #     self.response = self.client.get(reverse("books:display-books"))

    def test_status_code(self):
        response = self.client.get(reverse("books:display-books"))
        self.assertEqual(response.status_code, 200)

    def test_home_template(self):
        response = self.client.get(reverse("books:display-books"))
        self.assertTemplateUsed(response, "books/first_page.html")

    def test_no_book_displayed(self):
        user_1 = create_user("test", "test@test.com")
        create_books("abcd", timezone.now() +
                     datetime.timedelta(days=1), user_1)

        response = self.client.get(reverse("books:display-books"))
        self.assertQuerysetEqual(response.context.get("main_list"), [])
        self.assertQuerysetEqual(
            response.context.get("side_list"), [])

    def test_book_displayed(self):

        user_1 = create_user("test", "test@test.com")
        create_books("MyFirstBook", "1990-05-15", user_1)
        response = self.client.get(reverse("books:display-books"))

        self.assertQuerysetEqual(response.context.get(
            "main_list"), ["<Books: MyFirstBook de >"])
        self.assertQuerysetEqual(response.context.get(
            "side_list"), ["<Books: MyFirstBook de >"])

    def test_main_books(self):
        # ordering by price

        user_1 = create_user("test", "test@test.com")
        create_books("MyFreeBook", "1990-05-15", user_1)

        create_books("My10eBook", "1990-05-15", user_1, price=10)
        create_books("My15eBook", "2000-05-15", user_1, price=15)
        response = self.client.get(reverse("books:display-books"))

        self.assertQuerysetEqual(response.context.get(
            "main_list"), ["<Books: MyFreeBook de >", "<Books: My10eBook de >", "<Books: My15eBook de >"])

    def test_side_books(self):

        # ordering by date

        user_1 = create_user("test", "test@test.com")
        create_books("MyFirstBook", "1990-05-15", user_1)
        response = self.client.get(reverse("books:display-books"))
        create_books("MySecondBook", "2000-05-15", user_1)
        response = self.client.get(reverse("books:display-books"))

        self.assertQuerysetEqual(response.context.get(
            "side_list"), ["<Books: MySecondBook de >", "<Books: MyFirstBook de >"])

    def resolve(self):
        view = resolve("/books/home")
        self.assertEqual(view.func.__name__, "home_disokay_books")
        self.assertEqual(view.url_name, "display-books")
        self.assertEqual(view.app_names, ["books"])


class BookTests(TestCase):

    def setUp(self):

        self.user_1 = get_user_model().objects.create_user(
            username="test", email="test@test.com", date_of_birth="1992-03-12", password="testing1234")

        self.book = Books.objects.create(
            original_poster=self.user_1,
            title='Harry Potter',
            price='25.00',
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, 'Harry Potter')
        self.assertEqual(self.book.original_poster, self.user_1)
        self.assertEqual(self.book.price, '25.00')
