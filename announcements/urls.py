from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('create/', views.announcement_create, name='announcement_create'),
    path('<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('<int:pk>/update/', views.announcement_update, name='announcement_update'),
    path('<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('admin/', views.announcement_admin, name='announcement_admin'),  # New admin view for superusers
    # For SEO friendly URLs, you might add a slug later:
    # path('<int:pk>/<slug:slug>/', views.announcement_detail, name='announcement_detail_slug'),
]