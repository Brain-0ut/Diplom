# Generated by Django 3.1 on 2020-08-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(default='Title is enough')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'New'), (2, 'In progress'), (3, 'In QA'), (4, 'Ready'), (5, 'Done')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]