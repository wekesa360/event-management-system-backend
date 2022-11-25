from django.utils import timezone
from datetime import date
from django.conf import settings
from django.core.mail import send_mail as sm
from django.shortcuts import HttpResponse
from .models import Event
from django.contrib.auth import get_user_model

def event_status_check():
    events = Event.objects.all()
    for event in events:
        if f'{date.today()}' > f'{event.end_date}' and f'{timezone.now()}' >= f'{event.end_time}':
            event = Event.objects.get(event_title=event.event_title)
            event.status = 'completed'
            event.save()
            return HttpResponse(f'Today is: {date.today()} < event {event.event_title} closes on {event.end_date}>')
    return HttpResponse('Event end_date checker: <No event end_date is today or earlier>')

def get_emails(user_type):
    users = get_user_model().objects.filter(user_type=user_type)
    emails_dict = {}
    for user in users:
        emails_dict[user.first_name] = user.email
    return emails_dict

def send_signup_email(recipient):
    res = sm(
        subject = 'Event management system account signup',
        message = 'You have successfully registered an account with event management system!',
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [recipient.email],
        fail_silently=False,
    )
    return HttpResponse(f"Email sent to {res} members")

def send_signin_email(recipient):
    subject = 'Event management account signin'
    message = f'You have successfully signed into account {recipient.username}'
    res = sm(
        subject=subject,
        message=message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [recipient.email],
        fail_silently=False)
    return HttpResponse(f"Email sent to {res} members")

def send_new_event_email(emails_dict, event_details):
    for user_email in emails_dict:
        res  = sm(
          subject = 'EMS: New Event',
          message =  f'''Hi {user_email.key()}, \n A new Event has {event_details.event_title} has been created. \n
          sign in  and check it out''',
          from_email = settings.EMAIL_HOST_USER,
          recipient_list = [user_email.value()],
          fail_silently=True
        )
    return HttpResponse(f'Email sent to {res} members')