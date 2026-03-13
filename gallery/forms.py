from django import forms
from .models import Posts, Tag

class PostsForm(forms.ModelForm):
    class Meta: # This connects the form to a model
        model = Posts
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'custom-input'}),
            'content': forms.Textarea(attrs = {'class': 'custom-textarea'}),
            'image': forms.ClearableFileInput(attrs = {'class': 'custom-file-input'}),        
            'tags': forms.CheckboxSelectMultiple(),
    }
        

    