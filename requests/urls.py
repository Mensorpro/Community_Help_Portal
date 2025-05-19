from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create, name='request_create'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/update/', views.request_update, name='request_update'),
    path('<int:pk>/delete/', views.request_delete, name='request_delete'),
]