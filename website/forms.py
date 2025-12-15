"""
Forms for Kaffero showcase website.
"""

import random
from django import forms
from .models import DemoRequest, ContactMessage, NewsletterSubscriber


# Coffee-themed spam protection challenges
COFFEE_CHALLENGES = [
    {
        'question': 'What hot beverage is made from roasted beans?',
        'answers': ['coffee', 'cafe', 'kaffee', 'kaapi', 'kofi'],
        'hint': 'Hint: It starts with C',
    },
    {
        'question': 'Complete the word: Cof___',
        'answers': ['fee', 'coffee'],
        'hint': 'Hint: A popular morning drink',
    },
    {
        'question': 'What drink does a barista make?',
        'answers': ['coffee', 'cafe', 'espresso', 'latte', 'cappuccino'],
        'hint': 'Hint: Think cafe',
    },
    {
        'question': 'Espresso + steamed milk = ?',
        'answers': ['latte', 'cafe latte', 'caffe latte'],
        'hint': 'Hint: Rhymes with "atte"',
    },
    {
        'question': 'What is the Italian word for coffee?',
        'answers': ['caffe', 'cafe', 'caffè'],
        'hint': 'Hint: Starts with "caf"',
    },
]


class CoffeeChallengeMixin:
    """Mixin to add coffee-themed spam protection to forms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Select a random challenge
        challenge = random.choice(COFFEE_CHALLENGES)
        challenge_index = COFFEE_CHALLENGES.index(challenge)

        self.fields['coffee_challenge'] = forms.CharField(
            label=challenge['question'],
            required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': challenge['hint'],
                'autocomplete': 'off',
            }),
            help_text=challenge['hint']
        )

        # Store challenge index for validation
        self.fields['challenge_id'] = forms.IntegerField(
            widget=forms.HiddenInput(),
            initial=challenge_index
        )

    def clean(self):
        cleaned_data = super().clean()
        answer = cleaned_data.get('coffee_challenge', '').strip().lower()
        challenge_id = cleaned_data.get('challenge_id', 0)

        if challenge_id < 0 or challenge_id >= len(COFFEE_CHALLENGES):
            raise forms.ValidationError('Invalid challenge. Please refresh and try again.')

        challenge = COFFEE_CHALLENGES[challenge_id]
        valid_answers = [a.lower() for a in challenge['answers']]

        if answer not in valid_answers:
            raise forms.ValidationError(
                f"Oops! That's not quite right. {challenge['hint']}"
            )

        return cleaned_data


class DemoRequestForm(CoffeeChallengeMixin, forms.ModelForm):
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


class ContactForm(CoffeeChallengeMixin, forms.ModelForm):
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
