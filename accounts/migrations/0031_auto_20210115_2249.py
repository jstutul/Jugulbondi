# Generated by Django 2.2.7 on 2021-01-15 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20210115_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='p_city',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
