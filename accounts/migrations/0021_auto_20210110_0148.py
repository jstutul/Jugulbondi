# Generated by Django 2.2.7 on 2021-01-09 19:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_successstory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successstory',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
