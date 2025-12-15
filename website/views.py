"""
Views for Kaffero showcase website.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import (
    DemoRequest, ContactMessage, NewsletterSubscriber,
    Testimonial, FAQ, Feature, Screenshot, BlogPost,
    ChatConversation, ChatMessage
)
from .forms import DemoRequestForm, ContactForm, NewsletterForm, verify_turnstile
import json
import uuid
import re


def send_html_email(subject, template_name, context, to_email, from_email=None):
    """Send a beautiful HTML email with plain text fallback."""
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Render HTML content
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    # Create email with both HTML and plain text
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email] if isinstance(to_email, str) else to_email
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False


def home(request):
    """Home page view."""
    features = Feature.objects.filter(is_active=True, is_highlighted=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:3]

    context = {
        'features': features,
        'testimonials': testimonials,
    }
    return render(request, 'website/home.html', context)


def features(request):
    """Features page view."""
    features = Feature.objects.filter(is_active=True)
    screenshots = Screenshot.objects.filter(is_active=True)

    context = {
        'features': features,
        'screenshots': screenshots,
    }
    return render(request, 'website/features.html', context)


def feature_detail(request, slug):
    """Feature detail page view."""
    feature = get_object_or_404(Feature, slug=slug, is_active=True)
    related_features = Feature.objects.filter(is_active=True).exclude(id=feature.id)[:4]

    context = {
        'feature': feature,
        'related_features': related_features,
    }
    return render(request, 'website/feature_detail.html', context)


def pricing(request):
    """Pricing page view."""
    faqs = FAQ.objects.filter(category='pricing', is_active=True)

    context = {
        'faqs': faqs,
    }
    return render(request, 'website/pricing.html', context)


def demo(request):
    """Demo request page view."""
    if request.method == 'POST':
        form = DemoRequestForm(request.POST)

        # Verify Turnstile
        turnstile_token = request.POST.get('cf-turnstile-response', '')
        turnstile_valid = verify_turnstile(turnstile_token)

        if not turnstile_valid:
            messages.error(request, 'Please complete the security check.')
        elif form.is_valid():
            demo_request = form.save()

            # Email context
            email_context = {'demo_request': demo_request}

            # Send beautiful HTML email to admin
            send_html_email(
                subject=f'New Demo Request: {demo_request.cafe_name}',
                template_name='emails/admin_demo_notification.html',
                context=email_context,
                to_email=settings.ADMIN_EMAIL
            )

            # Send confirmation email to user (if email provided)
            if demo_request.email:
                send_html_email(
                    subject=f'Demo Request Confirmed - {demo_request.cafe_name}',
                    template_name='emails/demo_confirmation.html',
                    context=email_context,
                    to_email=demo_request.email
                )

            return redirect('demo_thank_you', pk=demo_request.pk)
    else:
        form = DemoRequestForm()

    screenshots = Screenshot.objects.filter(is_active=True)[:6]
    faqs = FAQ.objects.filter(category='demo', is_active=True)

    context = {
        'form': form,
        'screenshots': screenshots,
        'faqs': faqs,
    }
    return render(request, 'website/demo.html', context)


def demo_thank_you(request, pk):
    """Demo thank you page view."""
    demo_request = get_object_or_404(DemoRequest, pk=pk)

    context = {
        'demo_request': demo_request,
    }
    return render(request, 'website/demo_thank_you.html', context)


def about(request):
    """About page view."""
    return render(request, 'website/about.html')


def contact(request):
    """Contact page view."""
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Verify Turnstile
        turnstile_token = request.POST.get('cf-turnstile-response', '')
        turnstile_valid = verify_turnstile(turnstile_token)

        if not turnstile_valid:
            messages.error(request, 'Please complete the security check.')
        elif form.is_valid():
            contact_message = form.save()

            # Email context
            email_context = {'contact': contact_message}

            # Send beautiful HTML email to admin
            send_html_email(
                subject=f'Contact Form: {contact_message.get_subject_display()}',
                template_name='emails/admin_contact_notification.html',
                context=email_context,
                to_email=settings.ADMIN_EMAIL
            )

            # Send confirmation email to user
            send_html_email(
                subject='We received your message - Kaffero',
                template_name='emails/contact_confirmation.html',
                context=email_context,
                to_email=contact_message.email
            )

            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'website/contact.html', context)


def faq(request):
    """FAQ page view."""
    faqs = FAQ.objects.filter(is_active=True)
    categories = FAQ.Category.choices

    context = {
        'faqs': faqs,
        'categories': categories,
    }
    return render(request, 'website/faq.html', context)


def blog_list(request):
    """Blog list page view."""
    posts = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)

    context = {
        'posts': posts,
    }
    return render(request, 'website/blog_list.html', context)


def blog_detail(request, slug):
    """Blog post detail view."""
    post = get_object_or_404(BlogPost, slug=slug, status=BlogPost.Status.PUBLISHED)
    related_posts = BlogPost.objects.filter(
        status=BlogPost.Status.PUBLISHED
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'website/blog_detail.html', context)


def privacy(request):
    """Privacy policy page view."""
    return render(request, 'website/privacy.html')


def terms(request):
    """Terms and conditions page view."""
    return render(request, 'website/terms.html')


@require_POST
def newsletter_subscribe(request):
    """Newsletter subscription handler."""
    form = NewsletterForm(request.POST)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    # Regular form submission
    if form.is_valid():
        form.save()
        messages.success(request, 'Thank you for subscribing to our newsletter!')
    else:
        messages.error(request, 'This email is already subscribed.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_chatbot_response(user_message, conversation):
    """Generate a chatbot response based on user message."""
    message_lower = user_message.lower()

    # Greeting responses
    if any(word in message_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
        return "Hello! Welcome to Kaffero. I'm here to help you learn about our cafe management system. You can ask me about features, pricing, demo, or anything else!"

    # Pricing questions
    if any(word in message_lower for word in ['price', 'cost', 'pricing', 'how much', 'rate', 'fees']):
        return "Our pricing is simple and transparent:\n\n• **Starter**: ₹35,000 (1 outlet, 5 tables, 3 users)\n• **Standard**: ₹65,000 (3 outlets, 20 tables, 10 users) - Most Popular!\n• **Premium**: ₹95,000 (Unlimited everything)\n\nAll plans include **1 year free support**! After that, annual renewal is 20% of license + actual server/domain charges. Would you like a free demo?"

    # Demo questions
    if any(word in message_lower for word in ['demo', 'trial', 'try', 'test']):
        return "We offer a **free 7-day demo** personalized with your cafe name! You'll get access to:\n\n• Admin Dashboard\n• Waiter App (Android)\n• Kitchen Display\n• QR Menu\n\nWould you like to request a demo? Just click the 'Get Started' button or tell me your cafe name!"

    # Features questions
    if any(word in message_lower for word in ['feature', 'what can', 'capabilities', 'does it']):
        return "Kaffero is packed with features:\n\n• **Smart Orders** - Dine-in, takeaway, delivery\n• **Table Management** - Visual floor map with QR codes\n• **Kitchen Display** - Real-time orders, no paper!\n• **Waiter App** - Android app, works offline\n• **QR Ordering** - Customers scan and order\n• **Reports** - Sales, inventory, staff tracking\n\nWhich feature would you like to know more about?"

    # QR ordering
    if 'qr' in message_lower or 'scan' in message_lower:
        return "With **QR Ordering**, your customers can:\n\n1. Scan the QR code on their table\n2. Browse your beautiful digital menu\n3. Place orders directly from their phone\n4. No app download needed!\n\nThis reduces wait times and frees up your staff. Would you like a demo?"

    # Kitchen display
    if 'kitchen' in message_lower or 'kot' in message_lower:
        return "The **Kitchen Display System (KDS)** shows orders in real-time:\n\n• No more paper KOTs\n• Color-coded urgency\n• Order timers\n• Audio alerts\n• One-tap order bumping\n\nYour kitchen staff will love it!"

    # Support questions
    if any(word in message_lower for word in ['support', 'help', 'problem', 'issue']):
        return "We provide excellent support:\n\n• **Starter**: 6 months support\n• **Standard**: 1 year priority support\n• **Premium**: 2 years + on-site setup\n\nYou can reach us via WhatsApp, email, or phone. Our team typically responds within 2-4 hours!"

    # Contact info
    if any(word in message_lower for word in ['contact', 'phone', 'call', 'whatsapp', 'email']):
        return f"You can reach us at:\n\n📞 Phone: {settings.COMPANY_PHONE}\n💬 WhatsApp: {settings.COMPANY_WHATSAPP}\n📧 Email: {settings.COMPANY_EMAIL}\n\nWe typically respond within 2-4 hours during business hours!"

    # Cafe name detection (collecting lead info)
    if 'my cafe' in message_lower or 'cafe name' in message_lower or 'my restaurant' in message_lower:
        return "Great! I'd love to hear more about your cafe. What's your cafe name and city? This helps us personalize your demo experience!"

    # Thanks
    if any(word in message_lower for word in ['thank', 'thanks', 'thx']):
        return "You're welcome! Is there anything else you'd like to know about Kaffero? I'm happy to help!"

    # Bye
    if any(word in message_lower for word in ['bye', 'goodbye', 'see you']):
        return "Goodbye! Feel free to come back anytime. If you want to request a demo, just click the 'Get Started' button. Have a great day! ☕"

    # Default response
    return "Thanks for your message! I can help you with:\n\n• **Pricing** - Our plans and costs\n• **Features** - What Kaffero can do\n• **Demo** - Free trial information\n• **Support** - How we help you\n\nWhat would you like to know more about?"


@require_POST
def chatbot_message(request):
    """Handle chatbot messages."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', '')

        if not user_message:
            return JsonResponse({'success': False, 'error': 'Message is required'})

        # Create or get session ID
        if not session_id:
            session_id = str(uuid.uuid4())

        # Get or create conversation
        conversation, created = ChatConversation.objects.get_or_create(
            session_id=session_id,
            defaults={
                'page_url': request.META.get('HTTP_REFERER', ''),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'ip_address': get_client_ip(request),
            }
        )

        # Save user message
        ChatMessage.objects.create(
            conversation=conversation,
            role=ChatMessage.Role.USER,
            content=user_message
        )

        # Check if user is providing contact info
        # Email detection
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
        if email_match and not conversation.visitor_email:
            conversation.visitor_email = email_match.group()
            conversation.is_lead = True
            conversation.save()

        # Phone detection (Indian format)
        phone_match = re.search(r'(\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}', user_message)
        if phone_match and not conversation.visitor_phone:
            conversation.visitor_phone = phone_match.group()
            conversation.is_lead = True
            conversation.save()

        # Generate bot response
        bot_response = get_chatbot_response(user_message, conversation)

        # Save bot message
        ChatMessage.objects.create(
            conversation=conversation,
            role=ChatMessage.Role.BOT,
            content=bot_response
        )

        # Update conversation timestamp
        conversation.save()

        return JsonResponse({
            'success': True,
            'response': bot_response,
            'session_id': session_id
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def robots_txt(request):
    """Generate robots.txt for search engine crawlers."""
    content = """# Robots.txt for Kaffero - Cafe Management Software
# https://kaffero.online

User-agent: *
Allow: /

# Allow all major search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: YandexBot
Allow: /

# Allow AI crawlers
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: cohere-ai
Allow: /

# Disallow admin and dashboard areas
User-agent: *
Disallow: /admin/
Disallow: /dashboard/
Disallow: /api/

# Sitemap location
Sitemap: https://kaffero.online/sitemap.xml
Sitemap: https://www.kaffero.online/sitemap.xml

# Crawl-delay for politeness (optional)
Crawl-delay: 1
"""
    return HttpResponse(content, content_type='text/plain')


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def sitemap_xml(request):
    """Generate dynamic sitemap.xml for search engines."""
    from django.utils import timezone

    # Base URL
    base_url = "https://kaffero.online"

    # Static pages with priority and change frequency
    static_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'url': '/features/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/pricing/', 'priority': '0.9', 'changefreq': 'monthly'},
        {'url': '/demo/', 'priority': '0.9', 'changefreq': 'monthly'},
        {'url': '/about/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/contact/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/faq/', 'priority': '0.6', 'changefreq': 'monthly'},
        {'url': '/blog/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': '/privacy/', 'priority': '0.3', 'changefreq': 'yearly'},
        {'url': '/terms/', 'priority': '0.3', 'changefreq': 'yearly'},
    ]

    # Start XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Add static pages
    today = timezone.now().strftime('%Y-%m-%d')
    for page in static_pages:
        xml_content += f"""  <url>
    <loc>{base_url}{page['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>
"""

    # Add dynamic feature pages
    features = Feature.objects.filter(is_active=True)
    for feature in features:
        xml_content += f"""  <url>
    <loc>{base_url}/features/{feature.slug}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""

    # Add dynamic blog posts
    posts = BlogPost.objects.filter(status='published')
    for post in posts:
        lastmod = post.updated_at.strftime('%Y-%m-%d') if post.updated_at else today
        xml_content += f"""  <url>
    <loc>{base_url}/blog/{post.slug}/</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
"""

    xml_content += '</urlset>'

    return HttpResponse(xml_content, content_type='application/xml')
