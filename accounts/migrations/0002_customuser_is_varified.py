# Generated by Django 2.2.7 on 2020-12-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_varified',
            field=models.BooleanField(default=False),
        ),
    ]
