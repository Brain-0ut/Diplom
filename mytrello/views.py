from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, DeleteView

from mytrello import forms
from mytrello.models import Card
from users.models import User


def index(request):
    if request.user.id:
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.admin_confirmed:
            return redirect('homepage')
    return render(request, 'users/index.html')


class Index(ListView):
    model = Card
    template_name = 'mytrello/index.html'

    @classmethod
    def not_confirmed(cls):
        return User.objects.filter(admin_confirmed=False).count()

    def _filter(self, q):
        return q.filter(Q(assigned_to_user=self.request.user) | Q(created_by_user=self.request.user))

    def new(self):
        q = Card.objects.filter(status=1)
        if not self.request.user.is_superuser:
            q = self._filter(q)
        return q

    def in_progress(self):
        q = Card.objects.filter(status=2)
        if not self.request.user.is_superuser:
            q = self._filter(q)
        return q

    def in_qa(self):
        q = Card.objects.filter(status=3)
        if not self.request.user.is_superuser:
            q = self._filter(q)
        return q

    def ready(self):
        q = Card.objects.filter(status=4)
        if not self.request.user.is_superuser:
            q = self._filter(q)
        return q

    def done(self):
        q = Card.objects.filter(status=5)
        if not self.request.user.is_superuser:
            q = self._filter(q)
        return q

    def post(self, request, *args, **kwargs):
        card_id = request.POST.get('card_id', '')
        card = Card.objects.get(pk=card_id)
        action = request.POST.get('action')
        if action == 'next':
            card.status += 1
        elif action == 'back':
            card.status -= 1
        card.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewCardView(CreateView):
    model = Card
    form_class = forms.CardForm
    success_url = reverse_lazy('index')
    template_name = 'mytrello/new_card.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.status = 1
        self.object.created_by_user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['assigned_to_user'].queryset = User.objects.filter(id=self.request.user.id)
        return form


class EditCard(UpdateView):
    model = Card
    form_class = forms.CardForm
    success_url = reverse_lazy('index')
    template_name = 'mytrello/edit_card.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['assigned_to_user'].queryset = User.objects.filter(id=self.request.user.id)
        return form


class DeleteCard(DeleteView):
    model = Card
    form_class = forms.CardForm
    success_url = reverse_lazy('index')
    template_name = 'mytrello/delete_card.html'
