from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser
class PrettyAuthenticationForm(AuthenticationForm):
    """Extends Django AuthenticationForm: User signin form. """
    class Meta:
        widget = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }   

class ChangeImageForm(forms.Form):
    """ User Change Image Form. """
    avatar_image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': False, 'class': 'form-control'}))

class PrettyUserCreationForm(UserCreationForm):
    """ Extends Django UserCreationForm: User sign up form. """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), max_length=32, help_text='First name')
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), max_length=32, help_text='Last name')
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), max_length=64, help_text='Enter a valid email address')
    user_type = forms.ChoiceField(choices=CustomUser.TYPE_CHOICES,required=True, initial='Select')
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'user_type')

class RSVPForm(forms.Form):
    """User RSVP Form"""
    attending = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox', 'id':'attending'}))