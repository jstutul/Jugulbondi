# Generated by Django 2.2.7 on 2021-01-14 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='family_status',
            field=models.CharField(blank=True, choices=[('Reputed', 'Reputed'), ('Normal', 'Normal'), ('Medium', 'Medium')], max_length=30),
        ),
    ]
