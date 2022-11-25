
from .models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
from .functions import get_emails, send_new_event_email

@receiver(post_save, sender=Event)
def get_created_event(sender, instance, created, **kwargs):
    if created:
        event_details = Event.objects.get(id=instance.id)
        user_type = event_details.target_audience
        emails = get_emails(user_type)
        send_new_event_email(emails, event_details)

