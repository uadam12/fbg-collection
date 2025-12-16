from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from user.views import register, profile, edit_profile

app_name='user'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('reset-password/', PasswordResetView.as_view(template_name='auth/reset-password.html'), name='reset-password')
]