from django import forms
from .models import Announcement, AnnouncementCategory

class AnnouncementForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        help_text="Leave blank to publish immediately if 'Is Published' is checked. Otherwise, set a future date/time."
    )

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'category', 'is_published', 'published_at']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AnnouncementCategory.objects.all()
        self.fields['category'].required = False # As per model, category is optional