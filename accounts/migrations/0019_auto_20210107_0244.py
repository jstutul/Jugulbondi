# Generated by Django 2.2.7 on 2021-01-06 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_messeges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messeges',
            name='reply_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
