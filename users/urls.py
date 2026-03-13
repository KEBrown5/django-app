from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_page, name = 'login'),
    path('register/', views.register_page, name = 'register'),
    path('logout/', views.logout_page, name = 'logout'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('change_password/', views.change_password, name = 'change_password')
]