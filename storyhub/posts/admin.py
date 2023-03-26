from django.contrib import admin

from .models import BookmarkPost, LikePost, Post


admin.site.register(Post)
admin.site.register(BookmarkPost)
admin.site.register(LikePost)
