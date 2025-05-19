from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', next_page='core:home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'), # Moved this line up
    path('profile/<str:username>/', views.profile_view, name='profile_view'), # Moved this line down
]