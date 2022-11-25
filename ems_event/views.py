from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate, logout
from .forms import PrettyAuthenticationForm, PrettyUserCreationForm, RSVPForm, ChangeImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .functions import event_status_check, send_signup_email, send_signin_email
from django.urls import  reverse
from .models import (
    Event,
    EventSpeaker,
    CustomUser,
    SponsorOrPartner,
    Attendee
)

def signin_view(request):
    if request.method == 'POST':
        form = PrettyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                send_signin_email(user)
                messages.info(request, f'You are logged in!')
                return redirect('ems:home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    form = PrettyAuthenticationForm()
    return render(request, template_name='login.html', context={'form':form})

def signup_view(request):
    if request.method == 'POST':
        form = PrettyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_signup_email(user)
            messages.success(request, 'Signup successful')
            return redirect('ems:home')
        messages.error(request, 'Unsuccessful Signup. Invalid information.')
        return render(request, template_name='signup.html', context={'form': form})
    form = PrettyUserCreationForm
    return render(request, template_name='signup.html', context={'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have succcessfully logged out.')
    return redirect('ems:signin')

@login_required
def dasboard_view(request):
    try:
        user_email = request.user
        user_model = get_user_model()
        user = user_model.objects.get(email=user_email)
        events = Event.objects.filter(target_audience=user.user_type)
        active_events = Event.objects.filter(target_audience=user.user_type, status='active')
        attendee = Attendee.objects.filter(attendee=user)
        completed_events = []
        attending_events = []
        event_status_check()
        for person_instance in attendee:
            if person_instance.event.status == 'completed':
                completed_events.append(person_instance.event)
            if person_instance.event.status == 'active':
                attending_events.append(person_instance.event)
        completed_events = len(completed_events)
        attending_events = len(attending_events)
        if request.method == 'GET':
            form = ChangeImageForm()
            return render(request, 'index.html', context={'events': events,
                                                            'user': user,
                                                            'form': form,
                                                            'active_events': active_events,
                                                            'attending_events': attending_events,
                                                            'completed_events': completed_events})
        elif request.method == 'POST':
            form = ChangeImageForm(request.POST, request.FILES)
            if form.is_valid():
                user = CustomUser.objects.get(email=user.email)
                user.avatar = form.cleaned_data.get('avatar_image')
                user.save()
                form = ChangeImageForm()
                messages.success(request, 'Successfully changed image!')
                redirect('ems:home')
            else:
                form = ChangeImageForm()
                messages.error(request, 'Error saving file!')
                return render(request, 'index.html', context={'events': events, 
                                                            'user': user,
                                                            'form': form,
                                                            'attending_events': attending_events,
                                                            'completed_events': completed_events,})
        else:
            redirect('ems:home')
        redirect('ems:home')
    except ObjectDoesNotExist:
        print('Error getting Object')
        return redirect('ems:signin')
    return redirect('ems:signin')

@login_required
def event_view(request, slug):
    try:
        user_email = request.user
        user = get_user_model().objects.get(email=user_email)
        event = Event.objects.get(slug=slug)
        partners_or_sponsors = SponsorOrPartner.objects.filter(event=event)
        event_speakers = EventSpeaker.objects.filter(event=event)
        if request.method == 'GET':
            attendees = Attendee.objects.filter(event=event, attending=True)
            form = RSVPForm()
            return render(request, 'event.html', context={'speakers': event_speakers, 
                                                                'event': event,
                                                                'form': form,
                                                                'partners': partners_or_sponsors,
                                                                'attendees': attendees,})
        elif request.method == 'POST':
            form = RSVPForm(request.POST)
            
            if form.is_valid():
                Attendee.objects.get_or_create(attendee=user, 
                attending=form.cleaned_data.get('attending'), event=event)
                if_rsvped = Attendee.objects.filter(attendee=user, attending=True)
                if if_rsvped:
                    for rsvped_event in if_rsvped:
                        if rsvped_event.event == event:
                            messages.success(request, f'You will be attending {event.event_title}!')
                            return redirect(reverse('ems:event', kwargs={'slug': slug}))
                        elif rsvped_event.event == None:
                            rsvped_event.event = event
                            rsvped_event.save()
                        else:
                            print("There's an issue here!")
                    messages.success(request, f'See you at the {event.event_title} event!')
                    return redirect(reverse('ems:event', kwargs={'slug': slug}))
                messages.success(request, f'You will be attending {event.event_title}!')
                return redirect(reverse('ems:event', kwargs={'slug': slug}))
            else:
                messages.error(request, 'Oops something went wrong!')
                return redirect(reverse('ems:event', kwargs={'slug': slug}))
        return redirect('ems:home')
    except ObjectDoesNotExist:
        print('Error getting Object')
        return redirect('ems:home')