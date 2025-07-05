from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Username',
        'style': 'width: 100%; height: 50px; border-radius: 0;'}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder':'Password',
        'style': 'width: 100%; height: 50px; border-radius: 0;'}))

class RegistrationForm(UserCreationForm):
    label1=("Password")
    label2=("Password confirmation")
    password1 = forms.CharField(
            label=label1,
            required=False,
            strip=False,
            widget=forms.PasswordInput(attrs={
                "autocomplete": "new-password",
                'class': 'form-control',
                'placeholder':'Password',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
                }),
            help_text=password_validation.password_validators_help_text_html(),
        )
    password2 = forms.CharField(
            label=label2,
            required=False,
            widget=forms.PasswordInput(attrs={
                "autocomplete": "new-password",
                'class': 'form-control',
                'placeholder':'Confirm Password',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
                }),
            strip=False,
            help_text=("Enter the same password as before, for verification."),
        )
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            "username":forms.TextInput(attrs={
            "class":"form-control",
            'placeholder':'Your Name',
            'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            "email":forms.TextInput(attrs={
            "class":"form-control",
            'placeholder':'Email Address',
            'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            }


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
        'style': 'width: 100%; height: 50px; border-radius: 0;'
    }))