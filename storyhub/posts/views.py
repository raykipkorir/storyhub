import json

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, ListView
from users.models import UserProfile

from .forms import PostForm
from .models import Post

User = get_user_model()


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all
    template_name = "posts/post_list.html"
    context_object_name = "posts"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def post_detail_view(request, username, slug):
    # check if post exists if not raise Http404
    try:
        post = get_object_or_404(User, username=username).post_set.all().get(slug=slug)

        profile: UserProfile = get_object_or_404(UserProfile, user__username=username)
        current_user_profile = request.user.userprofile
        # request should be POST and user cannot follow himself/herself
        # same follow functionality as the one implemented in users app
        if request.method == "POST" and profile != current_user_profile:
            data = request.POST
            action = data.get("follow")
            if action == "follow":
                current_user_profile.follows.add(profile)
            elif action == "unfollow":
                current_user_profile.follows.remove(profile)
            current_user_profile.save()
            return redirect("post_detail", username=username, slug=post.slug)
        else:
            return render(request, "posts/post_detail.html", {"post": post, "profile": profile})
    except ObjectDoesNotExist:
        raise Http404
    

@login_required
def post_update_view(request, username, slug):
    # check if post exists if not raise Http404
    try:
        post = get_object_or_404(User, username=username).post_set.all().get(slug=slug)
        if request.user == post.user:
            form = PostForm(instance=post)
            if request.method == "POST":
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    form.save()
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
        post = get_object_or_404(User, username=username).post_set.all().get(slug=slug)
        if request.user == post.user:
            if request.method == "POST":
                post.delete()
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
