# Generated by Django 2.2.7 on 2021-01-01 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_followers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
