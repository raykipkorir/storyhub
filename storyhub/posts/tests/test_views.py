from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post

User = get_user_model()


class TestPostViews(TestCase):
    """Testing posts views"""

    def setUp(self) -> None:
        self.client = Client()
        self.user: User = User.objects.create_user(
            username="john", email="john@email.com", password="testing321"
        )
        self.user2: User = User.objects.create_user(
            username="jane", email="jane@email.com", password="testing321"
        )

        self.client.login(username="john", password="testing321")

        self.post: Post = Post.objects.create(
            user=self.user, title="My new post", content="Post content"
        )
        self.post2: Post = Post.objects.create(
            user=self.user2, title="My first post", content="Post content"
        )

    def test_post_list_view(self) -> None:
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_list.html")

    def test_post_create_view_GET(self) -> None:
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_create.html")

    def test_post_create_view_POST(self) -> None:
        response = self.client.post(
            reverse("post_create"),
            data={"title": "New post", "content": "Post content"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("post_detail", kwargs={"username": "john", "slug": "new-post"}),
        )

    def test_post_detail_view_GET(self) -> None:
        response = self.client.get(
            reverse(
                "post_detail",
                kwargs={"username": self.post.user.username, "slug": self.post.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")

    def test_post_detail_view_POST(self) -> None:
        response = self.client.post(reverse("post_detail", kwargs={"username": "jane", "slug": "my-first-post"}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post_detail", kwargs={"username": "jane", "slug": "my-first-post"}))

    def test_post_update_view_GET(self) -> None:
        response = self.client.get(
            reverse(
                "post_update",
                kwargs={"username": self.post.user.username, "slug": self.post.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_update.html")

    def test_post_update_view_POST(self) -> None:
        response = self.client.post(
            reverse(
                "post_update",
                kwargs={"username": self.post.user.username, "slug": self.post.slug},
            ),
            data={"title": self.post.title, "content": self.post.content},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "post_detail",
                kwargs={"username": self.post.user.username, "slug": self.post.slug},
            ),
        )

    def test_post_delete_view_GET(self) -> None:
        response = self.client.get(
            reverse(
                "post_delete",
                kwargs={"username": self.post.user.username, "slug": self.post.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_delete.html")

    def test_post_delete_view_POST(self) -> None:
        response = self.client.post(
            reverse(
                "post_delete",
                kwargs={"username": self.post.user.username, "slug": self.post.slug},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("user_profile", kwargs={"username": self.post.user.username}),
        )
