from django import forms
from account.models import *

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['name', 'phone_number', 'pincode', 'locality', 'address', 'district', 'state', 'address_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pincode',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            'locality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Locality',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'style': 'width: 100%; height: 150px; border-radius: 0;'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'District',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State',
                'style': 'width: 100%; height: 50px; border-radius: 0;'
            }),
            'address_type': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
        }



