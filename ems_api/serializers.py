from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from .utils import get_model_choices
from django.contrib.auth.models import BaseUserManager
from ems_event.models import (
    Category,
    EventSpeaker,
    Event,
    SponsorOrPartner,
    Attendee,

)

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.Serializer):
    auth_token = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'avatar', 'created_at', 'updated_at', 'auth_token', 'phone_number']
        read_only_fields = ['id', 'is_Active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'phone_number', 'created_at', 'updated_at']

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'password', 'phone_number']

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError('Email is already taken')
        return BaseUserManager.normalize_email(value)
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
    
class PasswordChangesSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('current password does not match')
        return value
    
    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class EventCategorySerializer(serializers.ModelSerializer):
    """
    event serializer
    """
    class Meta:
        model = Category
        fields = ['category', 'type', 'created_at', 'updated_at', 'slug']


    def validate_category_type(self, value):
        event_type = get_model_choices(Category.CATEGORY_CHOICES)
        if value not in event_type:
            raise ValueError('category type not allowed')
        return value


class EventSpeakerSerializer(serializers.ModelSerializer):
    """
    event speaker serializer
    """

    class Meta:
        model = EventSpeaker
        fields = ['first_name', 'last_name', 'company', 'title', 'bio', 'slug', 
        'avatar', 'created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    """
    event serializer
    """


    class Meta:
        model = Event
        fields = ['category', 'event_owner', 'event_title', 'description', 'event_type', 'start_date', 
        'end_date','event_type', 'start_time', 'end_time', 'speaker', 'target_audience', 'venue',
        'status', 'image', 'slug', 'created_at', 'updated_at']
    
    def validate_choices(self, model_choices, value):
        choices_list = get_model_choices(model_choices)
        if value not in choices_list:
            raise ValueError('choice not allowed')
        return value


class SponsorOrPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorOrPartner
        fields = ['event', 'name', 'logo', 'slug', 'created_at', 'updated_at']


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['attendee', 'event', 'attending', 'created_at', 'updated_at']