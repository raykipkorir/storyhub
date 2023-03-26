from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import user_profile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('allauth.urls')),
    path("settings/", include("users.urls")),
    path("", include("posts.urls")),

    path("@<str:username>/", user_profile, name="user_profile"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
