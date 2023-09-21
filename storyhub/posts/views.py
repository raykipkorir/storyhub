import json
from typing import Any

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, ListView
from users.models import UserProfile
from users.utils import follow_functionality

from .forms import PostForm
from .models import Post, PostViews

User = get_user_model()


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        posts = Post.objects.select_related("user").all()
        return posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        cache.clear()
        return super().form_valid(form)


def post_detail_view(request, username, slug):
    # check if post exists if not raise Http404
    try:
        post = Post.objects.select_related("user").get(slug=slug)
        profile = UserProfile.objects.select_related("user").get(user__username=username)
        # differentiating between anonymous user and logged-in user
        if hasattr(request.user, "userprofile"):
            current_user_profile = request.user.userprofile
        else:
            current_user_profile = None
            
        # request should be POST and user cannot follow himself/herself
        # same follow functionality as the one implemented in users app
        if request.method == "POST" and profile != current_user_profile and current_user_profile:
            data = request.POST
            action = data.get("follow")
            follow_functionality(action=action, profile=profile, current_user_profile=current_user_profile)
            cache.clear()
            return redirect("post_detail", username=username, slug=post.slug)
        else:
            # number of post views
            PostViews.objects.create(post=post)
            view_count = PostViews.objects.filter(post=post).count()
            context = {"post": post, "profile": profile, "view_count": view_count}
            return render(request, "posts/post_detail.html", context)
    except ObjectDoesNotExist:
        raise Http404
    

@login_required
def post_update_view(request, username, slug):
    # check if post exists if not raise Http404
    try:
        post = Post.objects.select_related("user").get(slug=slug)
        if request.user == post.user:
            form = PostForm(instance=post)
            if request.method == "POST":
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    form.save()
                    cache.clear()
                    return redirect("post_detail", username=request.user.username, slug=post.slug)
            return render(request, "posts/post_update.html", {"post": post})
        else:
            return redirect("post_list")
    except ObjectDoesNotExist:
        raise Http404


@login_required
def post_delete_view(request, username, slug):
    # check if post exists if not raise Http404
    try:
        post = Post.objects.select_related("user").get(slug=slug)
        if request.user == post.user:
            if request.method == "POST":
                post.delete()
                cache.clear()
                return redirect("user_profile", username=request.user.username)
        else:
            return redirect("post_list")
        return render(request, "posts/post_delete.html", {"post": post})
    except ObjectDoesNotExist:
        raise Http404
 
 
class ReactionView(LoginRequiredMixin, View):
    
    model = None
 
    def post(self, request, pk):
        # We need a user
        user = auth.get_user(request)
        # Trying to get a obj from the table, or create a new one
        obj, created = self.model.objects.get_or_create(user=user, post_id=pk)
        # If no new obj has been created,
        # Then we believe that the request was to delete the obj
        if not created:
            obj.delete()
 
        return HttpResponse(
            json.dumps({
                "created": created,
                "count": self.model.objects.filter(post_id=pk).count()
            }),
            content_type="application/json"
        )
    
    # get requests are sent on DOMContentLoad to retrieve reaction status
    def get(self, request, pk):
        user = auth.get_user(request)
        # checking the current logged in user has liked or bookmarked a post
        obj = self.model.objects.filter(user=user, post_id=pk).exists()
        return HttpResponse(
            json.dumps({
                "exists": obj,
                "count": self.model.objects.filter(post_id=pk).count()
            })
        )


def search_posts(request):
    if "q" in request.GET:
        query = request.GET.get("q")
        posts = Post.objects.select_related("user").filter(title__icontains=query)
    else:
        posts = Post.objects.select_related("user").all()
    return render(request, "posts/post_list.html", {"posts":posts})
