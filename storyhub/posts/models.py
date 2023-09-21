from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    cover_image = CloudinaryField("post_cover_images", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"username": self.user.username, "slug": self.slug})
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ["-updated_at"]
    

# class Comment(models.Model):
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)


class BookmarkPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering=["-created_at"]

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    