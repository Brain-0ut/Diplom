# Generated by Django 3.1 on 2020-08-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin_confirmed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
