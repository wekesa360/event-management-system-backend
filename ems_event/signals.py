
from .models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
from .functions import get_emails, send_new_event_email

@receiver(post_save, sender=Event)
def get_created_event(sender, instance, created, **kwargs):
    """Signal to check if new event instance is created

    Args:
        sender (model): model 
        instance (object): model object
        created (_type_): signal
    """
    if created:
        event_details = Event.objects.get(id=instance.id)
        user_type = event_details.target_audience
        emails = get_emails(user_type)
        send_new_event_email(emails, event_details)

