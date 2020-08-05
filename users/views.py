from datetime import timedelta, datetime, timezone

from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from users.forms import RegisterForm, EmailConfirmForm
from users.models import User
from AVShop import models

from django import views


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


def purchase_delete(request, purchase_id):
    count = 0
    if request.method == 'POST':
        purchase = models.Purchase.objects.get(id=purchase_id)
        count = models.Purchase.objects.count()
        a = purchase.created_at + timedelta(minutes=3)
        b = datetime.now().astimezone(timezone.utc)
        print(str(purchase.created_at) + '|' + str(count) + '|' + str(a) + '|' + str(b))
        if purchase.created_at + timedelta(minutes=3) >= datetime.now().astimezone(timezone.utc):
            refund = models.Refund(purchase=purchase)
            print(refund)
    return redirect('/users/personal/', {'count': count})


class UserInfo(View):
    template_name = 'users/personal_page.html'

    def get(self, request, *args, **kwargs):
        confirm_form = None
        purchase_list = models.Purchase.objects.filter(user=self.request.user.id)
        count = models.Purchase.objects.count()
        if not self.request.user.email_confirmed:
            confirm_form = EmailConfirmForm()
        return render(request, self.template_name, {'confirm_form': confirm_form,
                                                    'purchase_list': purchase_list,
                                                    'count': count,
                                                    })

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('action') == 'confirm':
            form = EmailConfirmForm(self.request.POST)
            if form.is_valid():
                if form.cleaned_data.get('token') == self.request.user.token:
                    self.request.user.email_confirmed = True
                    self.request.user.save()
            else:
                return render(self.request, self.template_name, {'confirm_form': form})
        return HttpResponseRedirect(reverse('user_info'))
