from django import forms
from .models import RequestPost, Response

class RequestPostForm(forms.ModelForm):
    class Meta:
        model = RequestPost
        fields = ['title', 'description', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }