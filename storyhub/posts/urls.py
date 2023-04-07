from django.urls import path
from posts.models import BookmarkPost, LikePost

from . import views

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("", views.PostListView.as_view(), name="post_list"),
    path("new/", views.PostCreateView.as_view(), name="post_create"),
    path("@<str:username>/<slug:slug>/", views.post_detail_view, name="post_detail"),
    path("@<str:username>/<slug:slug>/edit/", views.post_update_view, name="post_update"),
    path("@<str:username>/<slug:slug>/delete/", views.post_delete_view, name="post_delete"),

    path("<int:pk>/bookmark/", views.ReactionView.as_view(model=BookmarkPost), name="post_bookmark"),
    path("<int:pk>/like/", views.ReactionView.as_view(model=LikePost), name="post_like"),

    path("search/", views.search_posts, name="search_posts"),
]
