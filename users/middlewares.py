from time import time

from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import logout

SESSION_OFF_TIME = 300


class AdminConfirmUserRegisterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.admin_confirmed:
            messages.add_message(request, messages.WARNING, 'Треба дочекатися підтвердження адміністратора!')
        response = self.get_response(request)
        return response


class SessionExpiryHandleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        last_activity = request.session.get('last_activity')
        now = time()
        idle = now - last_activity if last_activity else 0

        if idle > SESSION_OFF_TIME:
            logout(request)
            return redirect('/')
        else:
            request.session['last_activity'] = now
            response = self.get_response(request)
            return response
