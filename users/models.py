import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    token = models.CharField(max_length=32, blank=True, null=True)
    admin_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        if not self.token:
            self.token = str(uuid.uuid4()).replace('-', '')
        return super(User, self).save(*args, **kwargs)
