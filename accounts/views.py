from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserProfileEditForm, UserEditForm
from .models import UserProfile
from requests.models import RequestPost, Response # Import RequestPost and Response

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure UserProfile is created upon registration
            UserProfile.objects.get_or_create(user=user) # Use get_or_create to be safe
            login(request, user)
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request, username):
    # Ensure UserProfile exists, create if not (e.g., for users created before UserProfile model)
    # This is more robustly handled by signals or upon user creation (like in register view)
    # For viewing, we fetch or 404 if user doesn't exist.
    # UserProfile should ideally always exist for an authenticated user.
    view_user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=view_user)

    # Add logic here if you want to display user's requests, responses, etc.
    # For example:
    user_requests = RequestPost.objects.filter(requester=view_user).order_by('-created_at')
    user_responses = Response.objects.filter(responder=view_user).order_by('-created_at') # Assuming you have a Response model

    context = {
        'view_user': view_user,
        'user_profile': user_profile,
        'user_requests': user_requests,
        'user_responses': user_responses,
    }
    return render(request, 'accounts/profile_view.html', context)

@login_required
def profile_edit(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user) # Get or create profile

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile has been updated successfully!') # Optional: add messages
            return redirect('accounts:profile_view', username=request.user.username)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'form_title': 'Edit Profile'
    }
    return render(request, 'accounts/profile_edit.html', context)
