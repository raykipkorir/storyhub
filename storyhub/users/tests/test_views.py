from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TestUserViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user: User = User.objects.create_user(
            username="john",
            email="john@email.com",
            password="testing321"
        )
        self.user2: User = User.objects.create_user(
            username="jane",
            email="jane@email.com",
            password="testing321"
        )
        self.client.login(username="john", password="testing321")

    def test_user_profile_view_GET(self) -> None:
        response = self.client.get(reverse("user_profile", kwargs={'username': "john"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_profile.html")

    def test_user_profile_view_POST(self) -> None:
        response = self.client.post(reverse("user_profile", kwargs={"username": "jane"}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_profile", kwargs={"username": "jane"}))

    def test_profile_update_view_GET(self) -> None:
        response = self.client.get(reverse("profile_update"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_update.html")

    def test_profile_update_view_POST(self) -> None:
        response = self.client.post(reverse("profile_update"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_update"))

    def test_user_update_view_GET(self) -> None:
        response = self.client.get(reverse("user_update"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_update.html")

    def test_user_update_view_POST(self) -> None:
        response = self.client.post(reverse("user_update"), data={"username": "ray", "full_name": "Raymond Kipkorir"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_update"))

    def test_user_delete_view_GET(self) -> None:
        response = self.client.get(reverse("user_delete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_delete.html")

    def test_user_delete_view_POST(self) -> None:
        response = self.client.post(reverse("user_delete"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post_list"))

    def test_follows_view_GET(self) -> None:
        response = self.client.get(reverse("follows", kwargs={"username": "jane"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/follows.html")

    def test_follows_view_POST(self) -> None:
        response = self.client.post(reverse("follows", kwargs={"username": "jane"}), data={"profile": "jane"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("follows", kwargs={"username": "jane"}))
