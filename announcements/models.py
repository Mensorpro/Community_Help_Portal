from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class AnnouncementCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Announcement Categories"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True, help_text="Set a future date to schedule publication, or leave blank to publish immediately if 'Is Published' is checked.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    is_published = models.BooleanField(default=False, help_text="Check this to make the announcement visible to users (respects 'Published At' date).")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at', '-created_at']