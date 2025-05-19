from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True) # Removed default

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def get_profile_picture_url(self):
        from django.conf import settings
        from django.templatetags.static import static

        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                # This will return the URL for the user's specific image,
                # or the URL for 'profile_pics/default.png' if that's what's stored in the field.
                return self.profile_picture.url
            except ValueError:
                # This might happen if the file is missing from storage
                # despite being referenced in the database.
                # Fall through to static default in this case.
                pass
        # Fallback if profile_picture field is None, has no URL, or .url access failed
        return static('images/default_profile.png')
