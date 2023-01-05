from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib import admin
from accounts.models import CustomUser
from .models import (
    Category,
    EventSpeaker,
    Event,
    SponsorOrPartner,
    Attendee
    )

admin.site.register(CustomUser)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'type')

@admin.register(EventSpeaker)
class EventSpeakerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company','title', 'avatar')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'category', 'event_type','start_date', 'end_date', 'target_audience')

@admin.register(SponsorOrPartner)
class SponsorOrPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'logo')

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'attending')