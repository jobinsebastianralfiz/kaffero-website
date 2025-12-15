"""
Models for Kaffero showcase website.
"""

from django.db import models
from django.utils import timezone


class DemoRequest(models.Model):
    """Model for tracking demo requests."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        DEMO_CREATED = 'demo_created', 'Demo Created'
        CONTACTED = 'contacted', 'Contacted'
        CONVERTED = 'converted', 'Converted'
        DECLINED = 'declined', 'Declined'

    class Source(models.TextChoices):
        GOOGLE = 'google', 'Google Search'
        SOCIAL_MEDIA = 'social_media', 'Social Media'
        REFERRAL = 'referral', 'Referral'
        JUST_DIAL = 'just_dial', 'Just Dial'
        WORD_OF_MOUTH = 'word_of_mouth', 'Word of Mouth'
        OTHER = 'other', 'Other'

    # Cafe Information
    cafe_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    num_tables = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Number of Tables'
    )
    num_outlets = models.PositiveIntegerField(
        default=1,
        verbose_name='Number of Outlets'
    )

    # Contact Information
    contact_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)

    # Lead Source
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER
    )

    # Demo Details
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    demo_url = models.URLField(blank=True, help_text='URL to the demo instance')
    demo_username = models.CharField(max_length=100, blank=True)
    demo_password = models.CharField(max_length=100, blank=True)
    demo_expires_at = models.DateTimeField(null=True, blank=True)

    # Additional Info
    notes = models.TextField(blank=True)
    message = models.TextField(blank=True, help_text='Message from the requester')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Communication tracking
    credentials_sent_at = models.DateTimeField(null=True, blank=True)
    last_contacted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Demo Request'
        verbose_name_plural = 'Demo Requests'

    def __str__(self):
        return f"{self.cafe_name} - {self.contact_name}"

    @property
    def is_demo_active(self):
        """Check if demo is still active."""
        if not self.demo_expires_at:
            return False
        return timezone.now() < self.demo_expires_at


class ContactMessage(models.Model):
    """Model for contact form submissions."""

    class Subject(models.TextChoices):
        GENERAL = 'general', 'General Inquiry'
        SALES = 'sales', 'Sales Inquiry'
        SUPPORT = 'support', 'Technical Support'
        PARTNERSHIP = 'partnership', 'Partnership'
        FEEDBACK = 'feedback', 'Feedback'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(
        max_length=20,
        choices=Subject.choices,
        default=Subject.GENERAL
    )
    message = models.TextField()

    # Status
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    """Model for newsletter subscriptions."""

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    """Model for customer testimonials."""

    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, help_text='e.g., Owner, Manager')
    cafe_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} - {self.cafe_name}"


class FAQ(models.Model):
    """Model for frequently asked questions."""

    class Category(models.TextChoices):
        GENERAL = 'general', 'General'
        PRICING = 'pricing', 'Pricing'
        DEMO = 'demo', 'Demo'
        FEATURES = 'features', 'Features'
        TECHNICAL = 'technical', 'Technical'
        SUPPORT = 'support', 'Support'

    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question[:100]


class Feature(models.Model):
    """Model for product features."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()
    icon = models.CharField(max_length=50, help_text='Heroicon name or emoji')
    image = models.ImageField(upload_to='features/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_highlighted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Feature bullet points (stored as JSON)
    bullet_points = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def __str__(self):
        return self.name


class Screenshot(models.Model):
    """Model for product screenshots."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='screenshots/')
    category = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Model for blog posts."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    author = models.CharField(max_length=100, default='Kaffero Team')
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated tags')

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def get_tags_list(self):
        """Return tags as a list."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]


class ChatConversation(models.Model):
    """Model for storing chatbot conversations."""

    session_id = models.CharField(max_length=100, db_index=True)
    visitor_name = models.CharField(max_length=200, blank=True)
    visitor_email = models.EmailField(blank=True)
    visitor_phone = models.CharField(max_length=20, blank=True)

    # Tracking
    page_url = models.URLField(blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Status
    is_resolved = models.BooleanField(default=False)
    is_lead = models.BooleanField(default=False, help_text='Mark if this is a potential lead')

    # Notes from admin
    admin_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Chat Conversation'
        verbose_name_plural = 'Chat Conversations'

    def __str__(self):
        name = self.visitor_name or 'Anonymous'
        return f"Chat with {name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def message_count(self):
        return self.messages.count()


class ChatMessage(models.Model):
    """Model for individual chat messages."""

    class Role(models.TextChoices):
        USER = 'user', 'User'
        BOT = 'bot', 'Bot'

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
