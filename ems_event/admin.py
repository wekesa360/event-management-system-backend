from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Category,
    EventSpeaker,
    Event,
    SponsorOrPartner,
    Attendee
    )
class UserAdmin(BaseUserAdmin):
  form = UserChangeForm
  fieldsets = (
      (None, {'fields': ('email', 'password', )}),
      (_('Personal info'), {'fields': ('first_name', 'last_name')}),
      (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
      (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {'fields': ('user_type', 'avatar')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('email', 'password1', 'password2'),
      }),
  )
  list_display = ['email', 'first_name', 'last_name', 'is_staff','user_type', 'avatar']
  search_fields = ('email', 'first_name', 'last_name')
  ordering = ('email', )
admin.site.register(CustomUser, UserAdmin)

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