from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import  reverse
from .models import (
    Event,
    EventSpeaker,
    Category,
    CustomUser,
    SponsorOrPartner,
    Attendee
)
SignupForm = ''

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are logged in!')
                return redirect('ems_event:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    form = AuthenticationForm()
    return render(request, template_name='login.html', context={'form':form})


def signup(request):
    if request.methos == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful')
            return redirect('ems_event:dashboard')
        messages.error(request, 'Unsuccessful Signup. Invalid information.')
    form = SignupForm
    return render(request, template_name='signup.html', context={'form': form})

def logout(request):
    logout(request)
    messages.info(request, 'You have succcessfully logged out.')
    return redirect('ems_event:login')

def password_reset(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = settings.AUTH_USER_MODEL.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    email_template_name = 'authentication/password/password_reset_email.text'
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Event Management System',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user':user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    # send to admin
                    try:
                        send_mail(subject, email, 'wekesa360@yahoo.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('/password_reset/done')
                messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request, template_name='authentication/password/password_reset.html',
                    context={'form': password_reset_form})
 
@login_required
def dasboard_view(request):
    try:
        user_id = request.user
        user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
        events = Event.objects.filter(target_audience=user.user_type)
        # for partners or sponsors, event_speaker, attendees 
        # loop through while conditioning with jinja
        partners_or_sponsors = SponsorOrPartner.objects.all()
        event_speaker = EventSpeaker()
        attendees = Attendee.objects.all()
        if request.method == 'GET':
            return render(request, 'dashboard.html', context={'events': events, 
                                                            'attendees': attendees,
                                                            'event_speaker':event_speaker,
                                                            'partners_or_sponsors': partners_or_sponsors})
        return redirect('ems_event:login')
    except ObjectDoesNotExist:
        print('Error getting Object')
        return redirect('ems_event: login')