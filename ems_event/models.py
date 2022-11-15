from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from autoslug import AutoSlugField


class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        ('lecturer', 'lecturer'),
        ('student', 'student')
    )
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    user_type = models.CharField(choices=TYPE_CHOICES)
    avatar = models.FileField(upload_to='user/uploads/avatar/')
    created_at = models.DateTimeField(auto_now_add=True)
    upadated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.first_name

    def get_avatar_url(self) -> str:
        return self.avatar.url


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('university', 'university'),
        ('school', 'school'),
        ('association', 'association'),
        ('class', 'class'),
        ('club', 'club')
    )
    category = models.CharField(max_length=80, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=256) # e.g roadtrip, cultural show, gala, webinar etc
    slug = AutoSlugField(populate_from='category', unique_with='id')
    created_at = models.DateTimeField(auto_add_now=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.category
    
    def get_absolute_url(self) -> str:
        return reverse("event:category", kwargs={"slug": self.slug})
    
    class Meta:
        db_table = 'categories'

class EventSpeaker(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    company = models.CharField(max_length=256)
    title = models.CharField(max_length=80, blank=True)
    bio = models.CharField(max_length=800, blank=True)
    slug = AutoSlugField(unique_with='id', populate_from='first_name')
    avatar = models.FileField(upload_to='speaker/uploads/avatar')
    created_at = models.DateTimeField(auto_add_now=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name
    
    def get_absolute_url(self):
        return reverse("event:speaker", kwargs={"slug": self.slug})

    def get_image_url(self):
        return self.avatar.url
    
    class Meta:
        db_table = 'speakers'
    

class Event(models.Model):
    TYPE_CHOICES = (
        ('online', 'online'),
        ('hybrid', 'hybrid'),
        ('physical', 'physical')
    )
    STATUS_CHOICES = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    TAGRGET_AUDIENCE_CHOICES = (
        ('students', 'Students'),
        ('lectuerers', 'Lecturers'),
        ('staff', 'Staff')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_title = models.TextField()
    description = models.TextField()
    event_type = models.CharField(max_length=80, choices=TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    speaker = models.ForeignKey(EventSpeaker, on_delete=models.CASCADE)
    target_audience = models.CharField(max_length=90, choices=TAGRGET_AUDIENCE_CHOICES)
    number_attendees = models.PositiveIntegerField(blank=True)
    venue = models.CharField(max_length=256) # if online, virtual link
    status = models.CharField(choices=STATUS_CHOICES, max_length=90)
    image = models.FileField(upload_to="event/uploads/images/")
    slug = AutoSlugField(populate_from='event_title', unique_with='id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def ___str__(self)-> str:
        return self.event_title
    
    def get_absolute_url(self):
        return reverse('ems_event:event', kwargs={'slug': self.slug})

    def get_image_url(self):
        return self.image.url

    class Meta:
        db_table = 'events'
    
class SponsorOrPartner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    logo = models.FileField(upload_to='sponsor_or_partner/uploads/logo')
    slug = AutoSlugField(populate_from='name', unique_with='id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("ems_event:sponsor_or_partner", kwargs={"slug": self.slug})
    
    def get_logo_url(self) -> str:
        return self.logo.url
    
    class Meta:
        db_table = 'sponsor_or_partners'


class Attendee(Models.Model):
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event)
    attending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        full_name = f'{self.attendee.first_name} {self.attendee.last_name}'
        return full_name
    
    def get_absolute_url(self):
        return reverse("ems_event:attendee", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['event']
        db_table = 'attendees'
