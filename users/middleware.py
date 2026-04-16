from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            if request.user.profile.is_banned:
                logout(request)
                messages.error(request, 'Ваш аккаунт заблокирован администратором.')
                return redirect('login')
        return self.get_response(request)
