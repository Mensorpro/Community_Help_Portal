from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Announcement, AnnouncementCategory
from .forms import AnnouncementForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # For pagination

# Helper function to check if user is superuser
def is_superuser(user):
    return user.is_superuser

def announcement_list(request):
    """
    Displays a list of published announcements, optionally filtered by category.
    """
    category_slug = request.GET.get('category')
    categories = AnnouncementCategory.objects.all()
    announcements_list = Announcement.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).select_related('category', 'author').order_by('-published_at', '-created_at')

    current_category = None
    if category_slug:
        current_category = get_object_or_404(AnnouncementCategory, slug=category_slug)
        announcements_list = announcements_list.filter(category=current_category)

    paginator = Paginator(announcements_list, 10) # Show 10 announcements per page
    page_number = request.GET.get('page')
    try:
        announcements = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        announcements = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        announcements = paginator.page(paginator.num_pages)
    
    context = {
        'announcements': announcements,
        'categories': categories,
        'current_category': current_category,
        'is_paginated': True if paginator.num_pages > 1 else False,
        'page_obj': announcements, # for pagination template tags
    }
    return render(request, 'announcements/announcement_list.html', context)

def announcement_detail(request, pk, slug=None):
    """
    Displays the detail of a single published announcement.
    Slug parameter is for potential future SEO-friendly URLs but PK is used for lookup.
    """
    # For superusers, show even unpublished announcements
    if request.user.is_superuser:
        announcement = get_object_or_404(
            Announcement.objects.select_related('category', 'author'),
            pk=pk
        )
    else:
        announcement = get_object_or_404(
            Announcement.objects.select_related('category', 'author'),
            pk=pk,
            is_published=True,
            published_at__lte=timezone.now()
        )
    return render(request, 'announcements/announcement_detail.html', {'announcement': announcement})

@login_required
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            # Superusers can directly publish if they want
            if request.user.is_superuser and 'publish_now' in request.POST:
                announcement.is_published = True
                announcement.published_at = timezone.now()
            announcement.save()
            return redirect('announcements:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/announcement_form.html', {'form': form, 'form_title': 'Create Announcement'})

@login_required
def announcement_update(request, pk):
    # Allow superusers to update any announcement
    if request.user.is_superuser:
        announcement = get_object_or_404(Announcement, pk=pk)
    else:
        announcement = get_object_or_404(Announcement, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            # Superusers can directly publish if they want
            if request.user.is_superuser and 'publish_now' in request.POST:
                announcement.is_published = True
                announcement.published_at = timezone.now()
            form.save()
            return redirect('announcements:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/announcement_form.html', {'form': form, 'form_title': 'Update Announcement'})

@login_required
def announcement_delete(request, pk):
    # Allow superusers to delete any announcement
    if request.user.is_superuser:
        announcement = get_object_or_404(Announcement, pk=pk)
    else:
        announcement = get_object_or_404(Announcement, pk=pk, author=request.user)
    
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements:announcement_list')
    return render(request, 'announcements/announcement_confirm_delete.html', {'announcement': announcement})

# New view for superusers to manage all announcements
@user_passes_test(is_superuser)
def announcement_admin(request):
    """
    Admin panel for superusers to see all announcements including unpublished ones
    """
    announcements = Announcement.objects.all().select_related('category', 'author').order_by('-created_at')
    now = timezone.now()  # Get current time for template to compare scheduled status
    return render(request, 'announcements/announcement_admin.html', {
        'announcements': announcements,
        'now': now,
    })