from allauth.account.models import EmailAddress
from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from posts.models import BookmarkPost, Post

from .forms import UserProfileForm, UserSignUpForm, UserUpdateForm
from .models import UserProfile


# overriding allauth's default signup view to use custom form
class UserSignUpView(SignupView):
    template_name = 'account/signup.html'
    form_class = UserSignUpForm
    success_url = reverse_lazy('account_login')


def user_profile(request, username: str):
    """ Profile page view"""

    profile: UserProfile = get_object_or_404(UserProfile, user__username=username)
    tab = request.GET.get("tab")
    if tab == "saved":
        bookmarked_posts = BookmarkPost.objects.filter(user__username=username)
        posts = [bookmarked_post.post for bookmarked_post in bookmarked_posts]
    else:
        posts = Post.objects.filter(user__username=username)
    return render(request, "users/user_profile.html", {"profile": profile, "posts": posts, "tab": tab})


@login_required
def profile_update(request):
    """ View for updating user's profile"""

    profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("user_update")
        
    return render(request, "users/profile_update.html", {"form": form})


@login_required
def user_update(request):
    """ View for updating user instance"""
    emails = EmailAddress.objects.filter(user=request.user)
    form = UserUpdateForm(instance=request.user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully")
            return redirect("user_update")
        
    return render(request, "users/user_update.html", {"form": form, "emails": emails})


@login_required()
def user_delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("post_list")
    return render(request, "users/user_delete.html")
