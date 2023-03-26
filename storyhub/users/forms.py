from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


class UserSignUpForm(SignupForm):
    """Create user form"""

    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full name"}))

    def save(self, request):
        user = super().save(request)
        full_name = self.cleaned_data["full_name"]
        user.full_name = full_name
        user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_pic", "bio", "location", "twitter_url", "personal_website"]
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "full_name"]
        