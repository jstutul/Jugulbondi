# Generated by Django 2.2.7 on 2021-01-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_successstory_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='successstory',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]
