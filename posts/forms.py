from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'link']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

