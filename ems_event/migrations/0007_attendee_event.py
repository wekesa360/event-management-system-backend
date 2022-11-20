# Generated by Django 4.1.3 on 2022-11-20 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ems_event', '0006_remove_attendee_event_alter_customuser_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ems_event.event'),
            preserve_default=False,
        ),
    ]
