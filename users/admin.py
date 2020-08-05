from django.contrib import admin

from mytrello import models as my_trello
from . import models


class CardsInline(admin.TabularInline):
    model = my_trello.Card
    fk_name = 'created_by_user'
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [CardsInline]
    list_display = ('username', 'token')


admin.site.register(models.User, UserAdmin)
