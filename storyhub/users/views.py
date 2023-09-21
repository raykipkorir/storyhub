from allauth.account.models import EmailAddress
from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Case, When
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from posts.models import BookmarkPost, Post

from .forms import UserProfileForm, UserSignUpForm, UserUpdateForm
from .models import UserProfile
from .utils import follow_functionality


# overriding allauth's default signup view to use custom form
class UserSignUpView(SignupView):
    template_name = 'account/signup.html'
    form_class = UserSignUpForm
    success_url = reverse_lazy('account_login')


def user_profile(request, username: str):
    """ Profile page view"""
    try:
        profile = UserProfile.objects.select_related("user").get(user__username=username)
    except UserProfile.DoesNotExist:
        raise Http404
    # differentiating between anonymous user and logged-in user
    if hasattr(request.user, "userprofile"):
        current_user_profile = request.user.userprofile
    else:
        current_user_profile = None
    
    # request should be POST and user cannot follow himself/herself
    if request.method == "POST" and profile != current_user_profile and current_user_profile:
        data = request.POST
        action = data.get("follow")
        follow_functionality(action=action, profile=profile, current_user_profile=current_user_profile)
        current_user_profile.save()
        cache.clear()
        return redirect("user_profile", username=username)
    else:
        tab = request.GET.get("tab")
        if tab == "saved":
            bookmarked_posts = BookmarkPost.objects.select_related("post", "user").filter(user__username=username)
            posts = [bookmarked_post.post for bookmarked_post in bookmarked_posts]
        else:
            posts = Post.objects.select_related("user").filter(user__username=username)
    return render(request, "users/user_profile.html", {"profile": profile, "posts": posts, "tab": tab})


@login_required
def profile_update(request):
    """ View for updating user's profile"""

    profile = UserProfile.objects.select_related("user").get(user=request.user)
    form = UserProfileForm(instance=profile)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            cache.clear()
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
            cache.clear()
            messages.success(request, "User updated successfully")
            return redirect("user_update")
        
    return render(request, "users/user_update.html", {"form": form, "emails": emails})


@login_required()
def user_delete(request):
    if request.method == "POST":
        request.user.delete()
        cache.clear()
        return redirect("post_list")
    return render(request, "users/user_delete.html")


def follows(request, username):
    # profile: UserProfile = get_object_or_404(UserProfile, user__username=username)
    try:
        profile = UserProfile.objects.select_related("user").get(user__username=username)
    except UserProfile.DoesNotExist:
        raise Http404
    # differentiating between anonymous user and logged-in user
    if hasattr(request.user, "userprofile"):
        current_user_profile = request.user.userprofile
    else:
        current_user_profile = None
        
    # request should be POST and user cannot follow himself/herself
    if request.method == "POST" and profile != current_user_profile and current_user_profile:
        data = request.POST
        action = data.get("follow")
        follow_functionality(action=action, profile=profile, current_user_profile=current_user_profile)
        current_user_profile.save()
        
        # obtaining value from hidden field so as to use profile username in the address bar ...
        # and not the one passed in action attribute in form tag.
        profile = request.POST.get("profile")
        # for some reason value from hidden field gets appended with 's , so i've stripped it 
        profile = profile.split("'")[0]

        cache.clear()
        return redirect("follows", username=profile)
    else:
        tab = request.GET.get("tab")
        if tab == "followers" or tab == None:
            # ordered to make sure logged in user is the first in the list of followers
            follows = profile.followed_by.order_by(Case(When(id=request.user.id, then=0), default=1))
        elif tab == "following":
            # ordered to make sure logged in user is the first in the list of following
            follows = profile.follows.order_by(Case(When(id=request.user.id, then=0), default=1))
        
        context = {
            "follows": follows,
            "profile": profile,
            "tab": tab,
        }
        return render(request, "users/follows.html", context)
