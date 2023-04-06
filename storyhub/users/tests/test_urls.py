from django.test import SimpleTestCase
from django.urls import resolve, reverse
from users import views


class TestUserUrls(SimpleTestCase):

    def test_user_profile_url(self) -> None:
        url: str = reverse("user_profile", kwargs={"username": "john"})
        self.assertEqual(resolve(url).func, views.user_profile)

    def test_profile_update_url(self) -> None:
        url: str = reverse("profile_update")
        self.assertEqual(resolve(url).func, views.profile_update)

    def test_user_update_url(self) -> None:
        url: str = reverse("user_update")
        self.assertEqual(resolve(url).func, views.user_update)
    
    def test_user_delete_url(self) -> None:
        url: str = reverse("user_delete")
        self.assertEqual(resolve(url).func, views.user_delete)

    def test_follows_url(self) -> None:
        url: str = reverse("follows", kwargs={"username": "john"})
        self.assertEqual(resolve(url).func, views.follows)
