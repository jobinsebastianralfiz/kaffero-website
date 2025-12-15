"""
Custom dashboard views for Kaffero admin panel.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.utils import timezone

from .models import (
    DemoRequest, ContactMessage, NewsletterSubscriber,
    Testimonial, FAQ, Feature, Screenshot, BlogPost,
    ChatConversation, ChatMessage
)
from .forms import DemoRequestForm, ContactForm


# =============================================================================
# Authentication Views
# =============================================================================

def dashboard_login(request):
    """Custom login page for dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard:home')
                return redirect(next_url)
            else:
                messages.error(request, 'You do not have permission to access the dashboard.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    """Logout and redirect to login page."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('dashboard:login')


# =============================================================================
# Dashboard Home
# =============================================================================

@login_required(login_url='dashboard:login')
def dashboard_home(request):
    """Dashboard home with stats and recent activity."""
    context = {
        'page_title': 'Dashboard',
        # Stats
        'demo_count': DemoRequest.objects.count(),
        'pending_demos': DemoRequest.objects.filter(status='pending').count(),
        'message_count': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'subscriber_count': NewsletterSubscriber.objects.filter(is_active=True).count(),
        'blog_count': BlogPost.objects.filter(status='published').count(),
        'feature_count': Feature.objects.filter(is_active=True).count(),
        'testimonial_count': Testimonial.objects.filter(is_active=True).count(),
        'screenshot_count': Screenshot.objects.filter(is_active=True).count(),
        'faq_count': FAQ.objects.filter(is_active=True).count(),
        # Recent items
        'recent_demos': DemoRequest.objects.order_by('-created_at')[:5],
        'recent_messages': ContactMessage.objects.filter(is_read=False).order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/home.html', context)


# =============================================================================
# Demo Requests Management
# =============================================================================

@login_required(login_url='dashboard:login')
def demo_list(request):
    """List all demo requests."""
    demos = DemoRequest.objects.all().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        demos = demos.filter(status=status_filter)

    # Search
    search = request.GET.get('search')
    if search:
        demos = demos.filter(cafe_name__icontains=search) | demos.filter(contact_name__icontains=search)

    paginator = Paginator(demos, 10)
    page = request.GET.get('page')
    demos = paginator.get_page(page)

    context = {
        'page_title': 'Demo Requests',
        'demos': demos,
        'status_choices': DemoRequest.Status.choices,
        'current_status': status_filter,
    }
    return render(request, 'dashboard/demos/list.html', context)


@login_required(login_url='dashboard:login')
def demo_detail(request, pk):
    """View and edit demo request details."""
    demo = get_object_or_404(DemoRequest, pk=pk)

    if request.method == 'POST':
        # Update demo details
        demo.status = request.POST.get('status', demo.status)
        demo.demo_url = request.POST.get('demo_url', demo.demo_url)
        demo.demo_username = request.POST.get('demo_username', demo.demo_username)
        demo.demo_password = request.POST.get('demo_password', demo.demo_password)
        demo.notes = request.POST.get('notes', demo.notes)

        if request.POST.get('demo_expires_at'):
            demo.demo_expires_at = request.POST.get('demo_expires_at')

        demo.save()
        messages.success(request, 'Demo request updated successfully.')
        return redirect('dashboard:demo_detail', pk=pk)

    context = {
        'page_title': f'Demo: {demo.cafe_name}',
        'demo': demo,
        'status_choices': DemoRequest.Status.choices,
    }
    return render(request, 'dashboard/demos/detail.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def demo_delete(request, pk):
    """Delete a demo request."""
    demo = get_object_or_404(DemoRequest, pk=pk)
    demo.delete()
    messages.success(request, 'Demo request deleted successfully.')
    return redirect('dashboard:demo_list')


# =============================================================================
# Contact Messages Management
# =============================================================================

@login_required(login_url='dashboard:login')
def message_list(request):
    """List all contact messages."""
    msgs = ContactMessage.objects.all().order_by('-created_at')

    # Filter by read status
    read_filter = request.GET.get('read')
    if read_filter == 'unread':
        msgs = msgs.filter(is_read=False)
    elif read_filter == 'read':
        msgs = msgs.filter(is_read=True)

    paginator = Paginator(msgs, 10)
    page = request.GET.get('page')
    msgs = paginator.get_page(page)

    context = {
        'page_title': 'Contact Messages',
        'messages_list': msgs,
        'current_filter': read_filter,
    }
    return render(request, 'dashboard/messages/list.html', context)


@login_required(login_url='dashboard:login')
def message_detail(request, pk):
    """View message details and mark as read."""
    msg = get_object_or_404(ContactMessage, pk=pk)

    # Mark as read
    if not msg.is_read:
        msg.is_read = True
        msg.save()

    if request.method == 'POST':
        if 'mark_replied' in request.POST:
            msg.is_replied = True
            msg.replied_at = timezone.now()
            msg.save()
            messages.success(request, 'Message marked as replied.')

    context = {
        'page_title': f'Message from {msg.name}',
        'msg': msg,
    }
    return render(request, 'dashboard/messages/detail.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def message_delete(request, pk):
    """Delete a message."""
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('dashboard:message_list')


# =============================================================================
# Blog Posts Management
# =============================================================================

@login_required(login_url='dashboard:login')
def blog_list(request):
    """List all blog posts."""
    posts = BlogPost.objects.all().order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        posts = posts.filter(status=status_filter)

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'page_title': 'Blog Posts',
        'posts': posts,
        'status_choices': BlogPost.Status.choices,
        'current_status': status_filter,
    }
    return render(request, 'dashboard/blog/list.html', context)


@login_required(login_url='dashboard:login')
def blog_create(request):
    """Create a new blog post."""
    if request.method == 'POST':
        post = BlogPost(
            title=request.POST.get('title'),
            slug=request.POST.get('slug'),
            excerpt=request.POST.get('excerpt'),
            content=request.POST.get('content'),
            status=request.POST.get('status', 'draft'),
            author=request.POST.get('author', 'Kaffero Team'),
            tags=request.POST.get('tags', ''),
            meta_title=request.POST.get('meta_title', ''),
            meta_description=request.POST.get('meta_description', ''),
        )

        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES['featured_image']

        if post.status == 'published':
            post.published_at = timezone.now()

        post.save()
        messages.success(request, 'Blog post created successfully.')
        return redirect('dashboard:blog_list')

    context = {
        'page_title': 'Create Blog Post',
        'status_choices': BlogPost.Status.choices,
    }
    return render(request, 'dashboard/blog/form.html', context)


@login_required(login_url='dashboard:login')
def blog_edit(request, pk):
    """Edit a blog post."""
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.slug = request.POST.get('slug')
        post.excerpt = request.POST.get('excerpt')
        post.content = request.POST.get('content')
        post.author = request.POST.get('author', 'Kaffero Team')
        post.tags = request.POST.get('tags', '')
        post.meta_title = request.POST.get('meta_title', '')
        post.meta_description = request.POST.get('meta_description', '')

        new_status = request.POST.get('status', 'draft')
        if new_status == 'published' and post.status != 'published':
            post.published_at = timezone.now()
        post.status = new_status

        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES['featured_image']

        post.save()
        messages.success(request, 'Blog post updated successfully.')
        return redirect('dashboard:blog_list')

    context = {
        'page_title': f'Edit: {post.title}',
        'post': post,
        'status_choices': BlogPost.Status.choices,
    }
    return render(request, 'dashboard/blog/form.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def blog_delete(request, pk):
    """Delete a blog post."""
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, 'Blog post deleted successfully.')
    return redirect('dashboard:blog_list')


# =============================================================================
# Features Management
# =============================================================================

@login_required(login_url='dashboard:login')
def feature_list(request):
    """List all features."""
    features = Feature.objects.all().order_by('order')

    context = {
        'page_title': 'Features',
        'features': features,
    }
    return render(request, 'dashboard/features/list.html', context)


@login_required(login_url='dashboard:login')
def feature_create(request):
    """Create a new feature."""
    if request.method == 'POST':
        feature = Feature(
            name=request.POST.get('name'),
            slug=request.POST.get('slug'),
            short_description=request.POST.get('short_description'),
            full_description=request.POST.get('full_description'),
            icon=request.POST.get('icon', ''),
            order=int(request.POST.get('order', 0)),
            is_highlighted=request.POST.get('is_highlighted') == 'on',
            is_active=request.POST.get('is_active') == 'on',
        )

        # Handle bullet points
        bullet_points = request.POST.getlist('bullet_points[]')
        feature.bullet_points = [bp for bp in bullet_points if bp.strip()]

        if request.FILES.get('image'):
            feature.image = request.FILES['image']

        feature.save()
        messages.success(request, 'Feature created successfully.')
        return redirect('dashboard:feature_list')

    context = {
        'page_title': 'Add Feature',
    }
    return render(request, 'dashboard/features/form.html', context)


@login_required(login_url='dashboard:login')
def feature_edit(request, pk):
    """Edit a feature."""
    feature = get_object_or_404(Feature, pk=pk)

    if request.method == 'POST':
        feature.name = request.POST.get('name')
        feature.slug = request.POST.get('slug')
        feature.short_description = request.POST.get('short_description')
        feature.full_description = request.POST.get('full_description')
        feature.icon = request.POST.get('icon', '')
        feature.order = int(request.POST.get('order', 0))
        feature.is_highlighted = request.POST.get('is_highlighted') == 'on'
        feature.is_active = request.POST.get('is_active') == 'on'

        # Handle bullet points
        bullet_points = request.POST.getlist('bullet_points[]')
        feature.bullet_points = [bp for bp in bullet_points if bp.strip()]

        if request.FILES.get('image'):
            feature.image = request.FILES['image']

        feature.save()
        messages.success(request, 'Feature updated successfully.')
        return redirect('dashboard:feature_list')

    context = {
        'page_title': f'Edit: {feature.name}',
        'feature': feature,
    }
    return render(request, 'dashboard/features/form.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def feature_delete(request, pk):
    """Delete a feature."""
    feature = get_object_or_404(Feature, pk=pk)
    feature.delete()
    messages.success(request, 'Feature deleted successfully.')
    return redirect('dashboard:feature_list')


# =============================================================================
# Screenshots Management
# =============================================================================

@login_required(login_url='dashboard:login')
def screenshot_list(request):
    """List all screenshots."""
    screenshots = Screenshot.objects.all().order_by('order')

    context = {
        'page_title': 'Screenshots',
        'screenshots': screenshots,
    }
    return render(request, 'dashboard/screenshots/list.html', context)


@login_required(login_url='dashboard:login')
def screenshot_create(request):
    """Create a new screenshot."""
    if request.method == 'POST':
        screenshot = Screenshot(
            title=request.POST.get('title'),
            description=request.POST.get('description', ''),
            category=request.POST.get('category', ''),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
        )

        if request.FILES.get('image'):
            screenshot.image = request.FILES['image']

        screenshot.save()
        messages.success(request, 'Screenshot added successfully.')
        return redirect('dashboard:screenshot_list')

    context = {
        'page_title': 'Add Screenshot',
    }
    return render(request, 'dashboard/screenshots/form.html', context)


@login_required(login_url='dashboard:login')
def screenshot_edit(request, pk):
    """Edit a screenshot."""
    screenshot = get_object_or_404(Screenshot, pk=pk)

    if request.method == 'POST':
        screenshot.title = request.POST.get('title')
        screenshot.description = request.POST.get('description', '')
        screenshot.category = request.POST.get('category', '')
        screenshot.order = int(request.POST.get('order', 0))
        screenshot.is_active = request.POST.get('is_active') == 'on'

        if request.FILES.get('image'):
            screenshot.image = request.FILES['image']

        screenshot.save()
        messages.success(request, 'Screenshot updated successfully.')
        return redirect('dashboard:screenshot_list')

    context = {
        'page_title': f'Edit: {screenshot.title}',
        'screenshot': screenshot,
    }
    return render(request, 'dashboard/screenshots/form.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def screenshot_delete(request, pk):
    """Delete a screenshot."""
    screenshot = get_object_or_404(Screenshot, pk=pk)
    screenshot.delete()
    messages.success(request, 'Screenshot deleted successfully.')
    return redirect('dashboard:screenshot_list')


# =============================================================================
# Testimonials Management
# =============================================================================

@login_required(login_url='dashboard:login')
def testimonial_list(request):
    """List all testimonials."""
    testimonials = Testimonial.objects.all().order_by('-is_featured', '-created_at')

    context = {
        'page_title': 'Testimonials',
        'testimonials': testimonials,
    }
    return render(request, 'dashboard/testimonials/list.html', context)


@login_required(login_url='dashboard:login')
def testimonial_create(request):
    """Create a new testimonial."""
    if request.method == 'POST':
        testimonial = Testimonial(
            name=request.POST.get('name'),
            role=request.POST.get('role'),
            cafe_name=request.POST.get('cafe_name'),
            city=request.POST.get('city'),
            content=request.POST.get('content'),
            rating=int(request.POST.get('rating', 5)),
            is_featured=request.POST.get('is_featured') == 'on',
            is_active=request.POST.get('is_active') == 'on',
        )

        if request.FILES.get('photo'):
            testimonial.photo = request.FILES['photo']

        testimonial.save()
        messages.success(request, 'Testimonial added successfully.')
        return redirect('dashboard:testimonial_list')

    context = {
        'page_title': 'Add Testimonial',
    }
    return render(request, 'dashboard/testimonials/form.html', context)


@login_required(login_url='dashboard:login')
def testimonial_edit(request, pk):
    """Edit a testimonial."""
    testimonial = get_object_or_404(Testimonial, pk=pk)

    if request.method == 'POST':
        testimonial.name = request.POST.get('name')
        testimonial.role = request.POST.get('role')
        testimonial.cafe_name = request.POST.get('cafe_name')
        testimonial.city = request.POST.get('city')
        testimonial.content = request.POST.get('content')
        testimonial.rating = int(request.POST.get('rating', 5))
        testimonial.is_featured = request.POST.get('is_featured') == 'on'
        testimonial.is_active = request.POST.get('is_active') == 'on'

        if request.FILES.get('photo'):
            testimonial.photo = request.FILES['photo']

        testimonial.save()
        messages.success(request, 'Testimonial updated successfully.')
        return redirect('dashboard:testimonial_list')

    context = {
        'page_title': f'Edit: {testimonial.name}',
        'testimonial': testimonial,
    }
    return render(request, 'dashboard/testimonials/form.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def testimonial_delete(request, pk):
    """Delete a testimonial."""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully.')
    return redirect('dashboard:testimonial_list')


# =============================================================================
# FAQ Management
# =============================================================================

@login_required(login_url='dashboard:login')
def faq_list(request):
    """List all FAQs."""
    faqs = FAQ.objects.all().order_by('category', 'order')

    context = {
        'page_title': 'FAQs',
        'faqs': faqs,
        'categories': FAQ.Category.choices,
    }
    return render(request, 'dashboard/faqs/list.html', context)


@login_required(login_url='dashboard:login')
def faq_create(request):
    """Create a new FAQ."""
    if request.method == 'POST':
        faq = FAQ(
            question=request.POST.get('question'),
            answer=request.POST.get('answer'),
            category=request.POST.get('category', 'general'),
            order=int(request.POST.get('order', 0)),
            is_active=request.POST.get('is_active') == 'on',
        )
        faq.save()
        messages.success(request, 'FAQ added successfully.')
        return redirect('dashboard:faq_list')

    context = {
        'page_title': 'Add FAQ',
        'categories': FAQ.Category.choices,
    }
    return render(request, 'dashboard/faqs/form.html', context)


@login_required(login_url='dashboard:login')
def faq_edit(request, pk):
    """Edit a FAQ."""
    faq = get_object_or_404(FAQ, pk=pk)

    if request.method == 'POST':
        faq.question = request.POST.get('question')
        faq.answer = request.POST.get('answer')
        faq.category = request.POST.get('category', 'general')
        faq.order = int(request.POST.get('order', 0))
        faq.is_active = request.POST.get('is_active') == 'on'
        faq.save()
        messages.success(request, 'FAQ updated successfully.')
        return redirect('dashboard:faq_list')

    context = {
        'page_title': f'Edit FAQ',
        'faq': faq,
        'categories': FAQ.Category.choices,
    }
    return render(request, 'dashboard/faqs/form.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def faq_delete(request, pk):
    """Delete a FAQ."""
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, 'FAQ deleted successfully.')
    return redirect('dashboard:faq_list')


# =============================================================================
# Newsletter Subscribers
# =============================================================================

@login_required(login_url='dashboard:login')
def subscriber_list(request):
    """List all newsletter subscribers."""
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')

    status_filter = request.GET.get('status')
    if status_filter == 'active':
        subscribers = subscribers.filter(is_active=True)
    elif status_filter == 'inactive':
        subscribers = subscribers.filter(is_active=False)

    paginator = Paginator(subscribers, 20)
    page = request.GET.get('page')
    subscribers = paginator.get_page(page)

    context = {
        'page_title': 'Newsletter Subscribers',
        'subscribers': subscribers,
        'current_filter': status_filter,
    }
    return render(request, 'dashboard/subscribers/list.html', context)


# =============================================================================
# Chat Conversations Management
# =============================================================================

@login_required(login_url='dashboard:login')
def chat_list(request):
    """List all chat conversations."""
    chats = ChatConversation.objects.all().order_by('-updated_at')

    # Filter by lead status
    lead_filter = request.GET.get('leads')
    if lead_filter == 'true':
        chats = chats.filter(is_lead=True)

    # Filter by resolved status
    resolved_filter = request.GET.get('resolved')
    if resolved_filter == 'true':
        chats = chats.filter(is_resolved=True)
    elif resolved_filter == 'false':
        chats = chats.filter(is_resolved=False)

    paginator = Paginator(chats, 20)
    page = request.GET.get('page')
    chats = paginator.get_page(page)

    context = {
        'page_title': 'Chat Conversations',
        'chats': chats,
        'lead_filter': lead_filter,
        'resolved_filter': resolved_filter,
    }
    return render(request, 'dashboard/chats/list.html', context)


@login_required(login_url='dashboard:login')
def chat_detail(request, pk):
    """View chat conversation details."""
    chat = get_object_or_404(ChatConversation, pk=pk)
    chat_messages = chat.messages.all().order_by('created_at')

    if request.method == 'POST':
        if 'mark_lead' in request.POST:
            chat.is_lead = True
            chat.save()
            messages.success(request, 'Marked as lead.')
        elif 'mark_resolved' in request.POST:
            chat.is_resolved = True
            chat.save()
            messages.success(request, 'Marked as resolved.')
        elif 'save_notes' in request.POST:
            chat.admin_notes = request.POST.get('admin_notes', '')
            chat.visitor_name = request.POST.get('visitor_name', '')
            chat.save()
            messages.success(request, 'Notes saved.')

    context = {
        'page_title': f'Chat #{chat.pk}',
        'chat': chat,
        'chat_messages': chat_messages,
    }
    return render(request, 'dashboard/chats/detail.html', context)


@login_required(login_url='dashboard:login')
@require_POST
def chat_delete(request, pk):
    """Delete a chat conversation."""
    chat = get_object_or_404(ChatConversation, pk=pk)
    chat.delete()
    messages.success(request, 'Chat conversation deleted.')
    return redirect('dashboard:chat_list')
