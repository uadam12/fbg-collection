from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "address", "profile_picture"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Address"}),
        }

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Last Name'
        })
    )
    email = forms.EmailField(
        required=True, label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email Address'
        })
    )
    password1 = forms.CharField(
        required=True, label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Enter a strong password',
        })
    )

    password2 = forms.CharField(
        required=True, label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Confirm your password',
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your default shipping address',
            'rows': 4
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'address')
