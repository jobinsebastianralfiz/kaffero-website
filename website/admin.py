"""
Admin configuration for Kaffero showcase website.
"""

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from .models import (
    DemoRequest, ContactMessage, NewsletterSubscriber,
    Testimonial, FAQ, Feature, Screenshot, BlogPost
)


class KafferoAdminSite(AdminSite):
    """Custom admin site with Kaffero branding."""
    site_header = 'Kaffero Admin'
    site_title = 'Kaffero Admin'
    index_title = 'Dashboard'

    def index(self, request, extra_context=None):
        """Custom admin index with dashboard stats."""
        extra_context = extra_context or {}

        # Get counts
        extra_context['demo_count'] = DemoRequest.objects.count()
        extra_context['message_count'] = ContactMessage.objects.count()
        extra_context['subscriber_count'] = NewsletterSubscriber.objects.filter(is_active=True).count()
        extra_context['blog_count'] = BlogPost.objects.count()
        extra_context['feature_count'] = Feature.objects.filter(is_active=True).count()
        extra_context['testimonial_count'] = Testimonial.objects.filter(is_active=True).count()
        extra_context['screenshot_count'] = Screenshot.objects.filter(is_active=True).count()
        extra_context['faq_count'] = FAQ.objects.filter(is_active=True).count()

        # Pending demos
        extra_context['pending_demos'] = DemoRequest.objects.filter(status='pending').count()

        # Recent demo requests
        extra_context['recent_demos'] = DemoRequest.objects.order_by('-created_at')[:5]

        # Unread messages
        extra_context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        extra_context['recent_messages'] = ContactMessage.objects.filter(is_read=False).order_by('-created_at')[:3]

        return super().index(request, extra_context)


# Create custom admin site instance
kaffero_admin = KafferoAdminSite(name='kaffero_admin')


class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ['cafe_name', 'contact_name', 'city', 'phone', 'status', 'created_at']
    list_filter = ['status', 'source', 'city', 'created_at']
    search_fields = ['cafe_name', 'contact_name', 'phone', 'email', 'city']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Cafe Information', {
            'fields': ('cafe_name', 'city', 'num_tables', 'num_outlets')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'phone', 'email', 'whatsapp')
        }),
        ('Lead Source', {
            'fields': ('source', 'message')
        }),
        ('Demo Details', {
            'fields': ('status', 'demo_url', 'demo_username', 'demo_password', 'demo_expires_at')
        }),
        ('Communication', {
            'fields': ('credentials_sent_at', 'last_contacted_at', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['subject', 'is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    ordering = ['-subscribed_at']


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'cafe_name', 'city', 'rating', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active', 'rating', 'city']
    search_fields = ['name', 'cafe_name', 'content']
    ordering = ['-is_featured', '-created_at']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    ordering = ['category', 'order']


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_highlighted', 'is_active']
    list_filter = ['is_highlighted', 'is_active']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order']


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'author', 'published_at', 'created_at']
    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']


# Register with custom admin site
kaffero_admin.register(DemoRequest, DemoRequestAdmin)
kaffero_admin.register(ContactMessage, ContactMessageAdmin)
kaffero_admin.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
kaffero_admin.register(Testimonial, TestimonialAdmin)
kaffero_admin.register(FAQ, FAQAdmin)
kaffero_admin.register(Feature, FeatureAdmin)
kaffero_admin.register(Screenshot, ScreenshotAdmin)
kaffero_admin.register(BlogPost, BlogPostAdmin)

# Also register with default admin site for compatibility
admin.site.register(DemoRequest, DemoRequestAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Screenshot, ScreenshotAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
