"""
Context processors for Kaffero website.
"""

import re
from django.conf import settings


def site_settings(request):
    """Add site settings to template context."""
    # Clean WhatsApp number for URL (remove +, spaces, dashes)
    whatsapp_clean = re.sub(r'[^\d]', '', settings.COMPANY_WHATSAPP)

    return {
        'site_name': settings.SITE_NAME,
        'site_tagline': settings.SITE_TAGLINE,
        'site_description': settings.SITE_DESCRIPTION,
        'company_name': settings.COMPANY_NAME,
        'company_email': settings.COMPANY_EMAIL,
        'company_phone': settings.COMPANY_PHONE,
        'company_whatsapp': settings.COMPANY_WHATSAPP,
        'company_whatsapp_url': whatsapp_clean,  # Clean version for wa.me links
        'company_address': settings.COMPANY_ADDRESS,
        'social_linkedin': settings.SOCIAL_LINKEDIN,
        'social_instagram': settings.SOCIAL_INSTAGRAM,
        'social_facebook': settings.SOCIAL_FACEBOOK,
        'social_youtube': settings.SOCIAL_YOUTUBE,
        'pricing': settings.PRICING,
    }
