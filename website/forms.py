"""
Forms for Kaffero showcase website.
"""

from django import forms
from .models import DemoRequest, ContactMessage, NewsletterSubscriber


class DemoRequestForm(forms.ModelForm):
    """Form for demo requests."""

    privacy_agreed = forms.BooleanField(
        required=True,
        label='I agree to the privacy policy'
    )

    class Meta:
        model = DemoRequest
        fields = [
            'cafe_name', 'city', 'num_tables',
            'contact_name', 'phone', 'email', 'source'
        ]
        widgets = {
            'cafe_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your cafe name'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City'
            }),
            'num_tables': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Approximate number'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com'
            }),
            'source': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        # Remove spaces and dashes
        phone = phone.replace(' ', '').replace('-', '')
        if not phone:
            raise forms.ValidationError('Phone number is required.')
        return phone


class ContactForm(forms.ModelForm):
    """Form for contact messages."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 5,
                'placeholder': 'Your message...'
            }),
        }


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription."""

    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email'
            })
        }
