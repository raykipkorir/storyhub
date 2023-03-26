from django.test import SimpleTestCase
from django.urls import resolve, reverse
from posts import views


class TestPostUrls(SimpleTestCase):
    """Testing posts urls"""

    def test_post_list_url(self) -> None:
        url: str = reverse("post_list")
        self.assertEqual(resolve(url).func.view_class, views.PostListView)

    def test_post_create_url(self) -> None:
        url: str = reverse("post_create")
        self.assertEqual(resolve(url).func.view_class, views.PostCreateView)
        
    def test_post_detail_url(self) -> None:
        url: str = reverse("post_detail", kwargs={"username": "john", "slug": "new-post"})
        self.assertEqual(resolve(url).func, views.post_detail_view)

    def test_post_update_url(self) -> None:
        url: str = reverse("post_update", kwargs={"username": "john", "slug": "new-post"})
        self.assertEqual(resolve(url).func, views.post_update_view)
    
    def test_post_delete_url(self) -> None:
        url: str = reverse("post_delete", kwargs={"username": "john", "slug": "new-post"})
        self.assertEqual(resolve(url).func, views.post_delete_view)

    def test_post_bookmark_url(self) -> None:
        url: str = reverse("post_bookmark", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, views.ReactionView)

    def test_post_like_url(self) -> None:
        url: str = reverse("post_like", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, views.ReactionView)
        