from django.contrib.auth import views as auth_views
from django.urls import path
from .forms import BannedAwareAuthenticationForm
from .views import profile_detail_view, profile_edit_view, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=BannedAwareAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('u/<slug:slug>/', profile_detail_view, name='profile_detail'),
]
