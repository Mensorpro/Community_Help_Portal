from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RequestCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Request Categories"

class RequestPost(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(RequestCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='request_posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    request_post = models.ForeignKey(RequestPost, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to '{self.request_post.title}' by {self.responder.username}"
