from django.db import models

from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


class Card(models.Model):
    STATUS_CHOICES = [(1, 'New'),
                      (2, "In progress"),
                      (3, "In QA"),
                      (4, 'Ready'),
                      (5, 'Done'),
                      ]
    created_by_user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL,
                                        blank=True, null=True, related_name='card_owner')
    assigned_to_user = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL,
                                         blank=True, null=True, related_name='card_executor')
    title = models.CharField(max_length=80)
    description = models.TextField(default='Title is enough')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
