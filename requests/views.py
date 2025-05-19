from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import RequestPost, Response, RequestCategory # Added RequestCategory
from .forms import RequestPostForm, ResponseForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # For pagination

# View to list all RequestPost
def request_list(request):
    request_posts_list = RequestPost.objects.all().order_by('-created_at')
    categories = RequestCategory.objects.all()
    status_choices = RequestPost.STATUS_CHOICES

    selected_category_slug = request.GET.get('category')
    selected_status = request.GET.get('status')

    if selected_category_slug:
        category = get_object_or_404(RequestCategory, slug=selected_category_slug)
        request_posts_list = request_posts_list.filter(category=category)
    
    if selected_status:
        request_posts_list = request_posts_list.filter(status=selected_status)

    paginator = Paginator(request_posts_list, 10) # Show 10 requests per page
    page_number = request.GET.get('page')
    try:
        request_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        request_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        request_posts = paginator.page(paginator.num_pages)

    context = {
        'request_posts': request_posts,
        'categories': categories,
        'status_choices': status_choices,
        'current_category_slug': selected_category_slug,
        'current_status': selected_status,
        'is_paginated': True if paginator.num_pages > 1 else False,
        'page_obj': request_posts, # for pagination template tags
    }
    return render(request, 'requests/request_list.html', context)

# View for RequestPost detail, including responses
def request_detail(request, pk):
    request_post = get_object_or_404(RequestPost, pk=pk)
    responses = request_post.responses.all().order_by('created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login') # Assuming 'accounts:login' is your login URL
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            new_response = response_form.save(commit=False)
            new_response.request_post = request_post
            new_response.responder = request.user
            new_response.save()
            return redirect('requests:request_detail', pk=pk) # Assuming 'requests:request_detail'
    else:
        response_form = ResponseForm()
    return render(request, 'requests/request_detail.html', {
        'request_post': request_post,
        'responses': responses,
        'response_form': response_form
    })

# View for creating a new RequestPost
@login_required
def request_create(request):
    if request.method == 'POST':
        form = RequestPostForm(request.POST)
        if form.is_valid():
            request_post = form.save(commit=False)
            request_post.requester = request.user
            request_post.save()
            return redirect('requests:request_detail', pk=request_post.pk) # Redirect to the new post's detail view
    else:
        form = RequestPostForm()
    # Explicitly pass the current app namespace to the template context
    return render(request, 'requests/request_form.html', {
        'form': form,
        'form_title': 'Create Help Request',
        'current_app': request.resolver_match.namespace
    })

# View for updating an existing RequestPost
@login_required
def request_update(request, pk):
    request_post = get_object_or_404(RequestPost, pk=pk)
    if request_post.requester != request.user:
        return HttpResponseForbidden("You are not allowed to edit this request.")
    if request.method == 'POST':
        form = RequestPostForm(request.POST, instance=request_post)
        if form.is_valid():
            form.save()
            return redirect('requests:request_detail', pk=request_post.pk)
    else:
        form = RequestPostForm(instance=request_post)
    return render(request, 'requests/request_form.html', {'form': form, 'form_title': 'Update Help Request'})

# View for deleting a RequestPost
@login_required
def request_delete(request, pk):
    request_post = get_object_or_404(RequestPost, pk=pk)
    if request_post.requester != request.user:
        return HttpResponseForbidden("You are not allowed to delete this request.")
    if request.method == 'POST':
        request_post.delete()
        return redirect('requests:request_list') # Redirect to the list of requests
    return render(request, 'requests/request_confirm_delete.html', {'request_post': request_post})

# View for adding a Response to a RequestPost (handled within request_detail for simplicity now)
# If more complex logic is needed for adding a response, a separate view can be created.
# For example, if you wanted a dedicated page for writing a response.
