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
        print("files", self.request.FILES)
        form.instance.user = self.request.user
        return super().form_valid(form)


def post_detail_view(request, username, slug):
    try:
        post = get_object_or_404(User, username=username).post_set.all().get(slug=slug)
        return render(request, "posts/post_detail.html", {"post": post})
    except ObjectDoesNotExist:
        raise Http404
    

@login_required
def post_update_view(request, username, slug):
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
        # Trying to get a bookmark from the table, or create a new one
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
    
    def get(self, request, pk):
        user = auth.get_user(request)
        obj = self.model.objects.filter(user=user, post_id=pk).exists()
        return HttpResponse(
            json.dumps({
                "exists": obj,
                "count": self.model.objects.filter(post_id=pk).count()
            })
        )
