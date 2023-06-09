from django import forms
from django.forms import ModelForm

from catalog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'preview', 'is_published')