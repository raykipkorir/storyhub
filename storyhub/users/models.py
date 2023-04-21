from cloudinary.models import CloudinaryField
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.db import models
from django.urls import reverse
from django.utils import timezone

# custom user
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(verbose_name="email address", unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField(default=timezone.now)

    # EMAIL_FIELD = "username"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()
    

# UserProfile model 
class UserProfile(models.Model):
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    twitter_url = models.URLField(verbose_name="Twitter", blank=True, null=True)
    personal_website = models.URLField(verbose_name="Website", blank=True, null=True)
    profile_pic = CloudinaryField("profile_pics", blank=True, null=True)
    
    # symmetrical=False so that users can follow someone without them following back automatically
    # blank=True users don't need to follow anyone
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"username": self.user.username})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
