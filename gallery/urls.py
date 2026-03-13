from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

app_name = 'blogsite'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:pk>/', views.posts_detail, name='posts_detail'),
    path('<int:pk>/edit/', views.edit_posts, name='edit_posts'),
    path('<int:pk>/delete/', views.delete_posts, name='delete_posts'),
    path('about/', views.about, name='about'),
    path('account/', views.account, name ='account'),
    path('create/', views.create, name = 'create'),
]