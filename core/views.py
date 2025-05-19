from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from announcements.models import Announcement
from requests.models import RequestPost # Import RequestPost

# Create your views here.
def home(request):
    now = timezone.now()
    # Fetch top 3 published announcements
    recent_announcements = Announcement.objects.filter(
        is_published=True,
        published_at__lte=now
    ).order_by('-published_at', '-created_at')[:3] # Explicitly order if not relying on model meta

    # Fetch top 3 recent 'open' or 'in_progress' help requests
    recent_requests = RequestPost.objects.filter(
        Q(status='open') | Q(status='in_progress')
    ).order_by('-created_at')[:3]

    context = {
        'recent_announcements': recent_announcements,
        'recent_requests': recent_requests, # Add recent requests to context
    }
    return render(request, 'core/home.html', context)
