from django.shortcuts import render

from mytrello.models import Card
from users.models import User


def index(request):
    if request.user.id:
        user = User.objects.get(id=request.user.id)
        not_confirmed = User.objects.filter(admin_confirmed=False).count()
        if request.user.is_authenticated and user.admin_confirmed:
            context = Card.objects.filter(created_by_user=user.id)
            return render(request, 'mytrello/index.html', {'context': context, 'not_confirmed': not_confirmed})
    return render(request, 'users/index.html')
