from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Profile
from django.urls import reverse, resolve
from .views import SignUpPageView
from .forms import PersoUserRegisterForm, ProfileUpdateForm, PersoUserUpdateForm


class test_user_creation(TestCase):

    def test_create_user(self):

        User = get_user_model()

        new_user = User.objects.create_user(
            username="New_user", email="New_user@user.com", date_of_birth="2002-12-23")

        self.assertEqual(new_user.username, "New_user")
        self.assertEqual(new_user.email, "New_user@user.com")
        self.assertEqual(new_user.date_of_birth, "2002-12-23")
        self.assertIs(new_user.is_admin, False)
        self.assertIs(new_user.is_staff, False)
        self.assertEqual(new_user.profile, Profile.objects.get(user=new_user))

    def test_create_super_user(self):

        User = get_user_model()

        new_user = User.objects.create_superuser(
            username="New_super_user", email="New_super_user@user.com", date_of_birth="2002-12-23")

        self.assertEqual(new_user.username, "New_super_user")
        self.assertEqual(new_user.email, "New_super_user@user.com")
        self.assertEqual(new_user.date_of_birth, "2002-12-23")
        self.assertIs(new_user.is_admin, True)
        self.assertIs(new_user.is_staff, True)
        self.assertEqual(new_user.profile, Profile.objects.get(user=new_user))


class test_register_page(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("users:register"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "users/register.html")

    def test_html(self):
        self.assertContains(self.response, "Register")

    def test_register_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, PersoUserRegisterForm)

    def test_resolve(self):
        view = resolve("/users/register/")

        self.assertEqual(view.func.__name__, "SignUpPageView")
        self.assertEqual(view.url_name, "register")
        self.assertEqual(view.app_names, ["users"])


class test_profile_page(TestCase):

    def setUp(self):
        # Create user
        user_1 = get_user_model().objects.create_user(
            username="test", email="test@test.com", date_of_birth="1992-03-12", password="testing1234")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("users:update_profile"))
        self.assertNotEqual(response.status_code, 400)
        self.assertRedirects(
            response, "/accounts/login/?next=/users/update_profile/")

    def test_succes_if_logged_in(self):
        login = self.client.login(
            email="test@test.com", password="testing1234")
        response = self.client.get(reverse("users:update_profile"))
        view = resolve("/users/update_profile/")

        self.assertEqual(response.context.get("user").email, "test@test.com")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/private_profile.html")
        self.assertContains(response,  "Username")
        self.assertIsInstance(response.context.get(
            "u_form"), PersoUserUpdateForm)

        self.assertEqual(view.func.__name__, "private_profile")
        self.assertEqual(view.url_name, "update_profile")
        self.assertEqual(view.app_names, ["users"])
