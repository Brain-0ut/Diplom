from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework import viewsets

from users import models
from users.api.serializers import UserSerializer
from users.forms import RegisterForm, LoginForm
from users.models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'users/register.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


def confirm(request):
    pass


class UserListView(ListView):
    model = models.User
    template_name = 'users/user_list.html'

    @staticmethod
    def not_confirmed():
        return User.objects.filter(admin_confirmed=False).count()

    def post(self, request, *args, **kwargs):
        not_confirmed_user = models.User.objects.get(pk=request.POST.get('user_id'))
        action = request.POST.get('action')
        if action == 'confirm':
            not_confirmed_user.admin_confirmed = True
            not_confirmed_user.save()
        not_conf = self.not_confirmed
        if not_conf:
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('/')

    def get(self, request, *args, **kwargs):
        if self.not_confirmed():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('/')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

