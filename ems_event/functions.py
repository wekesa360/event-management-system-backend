from django.utils import timezone
from datetime import date
from django.conf import settings
from django.core.mail import send_mail as sm
from django.template.loader import render_to_string
from .models import Event
from django.contrib.auth import get_user_model

def event_status_check():
    events = Event.objects.all()
    for event in events:
        if f'{date.today()}' > f'{event.end_date}' and f'{timezone.now()}' >= f'{event.end_time}':
            event = Event.objects.get(event_title=event.event_title)
            event.status = 'completed'
            event.save()
            print(f'Today is: {date.today()} <event: {event.event_title} closes on {event.end_date}>')
    print('Event end_date checker: <No event end_date is today or earlier>')

def get_emails(user_type):
    users = get_user_model().objects.filter(user_type=user_type)
    emails_dict = {}
    for user in users:
        emails_dict[user.first_name] = user.email
    return emails_dict

def send_signup_email(recipient):
    msg_html = render_to_string('email/email_signup.html', {'username': recipient.username,
                                                  'email': recipient.email})
    res = sm(
        subject = 'Event management system account signup',
        message = '',
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [recipient.email],
        html_message=msg_html,
        fail_silently=False,
    )
    print(f"Email sent to {res} members")

def send_signin_email(recipient):
    subject = 'Event management account signin'
    message = ''
    msg_html = render_to_string('email/email_signin.html', {'username':recipient.username,
                                                            'email': recipient.email})
    res = sm(
        subject=subject,
        message=message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [recipient.email],
        html_message=msg_html,
        fail_silently=False
    )
    print(f"Email sent to {res} members")

def send_new_event_email(emails_dict, event_details):
    email_list = []
    for user in emails_dict:
        email_list.append(emails_dict[user])
    print(email_list)
    msg_html = render_to_string('email/email_event.html', {'event': event_details})
    res  = sm(
        subject = 'Event Management System: New Event',
        message =  '',
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = email_list,
        html_message=msg_html,
        fail_silently=True
    )
    print(f'Email sent')