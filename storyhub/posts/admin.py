from django.contrib import admin

from .models import BookmarkPost, LikePost, Post, PostViews


admin.site.register(Post)
admin.site.register(BookmarkPost)
admin.site.register(LikePost)
admin.site.register(PostViews)
