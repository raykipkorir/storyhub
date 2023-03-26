from django.urls import path

from . import views

urlpatterns = [    
    path("", views.profile_update, name="profile_update"),
    path("profile/", views.profile_update, name="profile_update"),
    path("account/", views.user_update, name="user_update"),
    path("account/delete/", views.user_delete, name="user_delete"),
]
