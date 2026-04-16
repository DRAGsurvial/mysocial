from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', slug=profile.slug)
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})

def profile_detail_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    channels = profile.user.channels.all().order_by('-created_at')
    return render(request, 'users/profile.html', {'profile': profile, 'channels': channels})
