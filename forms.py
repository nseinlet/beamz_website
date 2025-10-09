from django import forms
from django.utils.translation import gettext as _

from beamz_auth.fields import CaptchaField


class ContactUsForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': ''
        }))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control', 
            'placeholder': '',
            'required': True
        }))
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control', 
            'placeholder': '',
            'rows': 5
        }))
    captcha = CaptchaField()
