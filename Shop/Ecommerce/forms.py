
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from .models import Address


# User Profile Form
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

# Address Form
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        exclude = ['user', 'created_at', 'updated_at']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),

            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number'
            }),

            'address_line': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'House No, Street, Building'
            }),

            'landmark': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Landmark'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),

            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),

            'pin_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PIN Code'
            }),

            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'address_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'is_default': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# Password Form
class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        })
    )

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )

    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
