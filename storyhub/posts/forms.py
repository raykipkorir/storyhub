from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ["cover_image", "title", "content"]
        
    # validating title length
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < settings.POST_TITLE_MIN_LENGTH:
            raise ValidationError(f"Title is less than {settings.POST_TITLE_MIN_LENGTH} chars")
        return title
        