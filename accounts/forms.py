from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',) # Added first_name and last_name

from .models import UserProfile

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'contact_info', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class UserEditForm(forms.ModelForm): # For editing User model fields like name, email
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']