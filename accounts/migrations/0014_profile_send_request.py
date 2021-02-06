# Generated by Django 2.2.7 on 2021-01-04 18:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_profile_see_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='send_request',
            field=models.ManyToManyField(blank=True, related_name='send_request', to=settings.AUTH_USER_MODEL),
        ),
    ]
