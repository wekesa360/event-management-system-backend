# Generated by Django 4.1.3 on 2022-11-17 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems_event', '0002_remove_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
