from django import forms

from mytrello import models


class CardForm(forms.ModelForm):

    class Meta:
        model = models.Card
        fields = ('title', 'description', 'assigned_to_user')
        labels = {
                 'title': 'Назва',
                 'description': 'Детальний опис',
                 'assigned_to_user': 'Виконавець',
        }

