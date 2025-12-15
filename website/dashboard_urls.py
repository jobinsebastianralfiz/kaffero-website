"""
URL configuration for Kaffero custom dashboard.
"""

from django.urls import path
from . import dashboard_views as views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),

    # Dashboard home
    path('', views.dashboard_home, name='home'),

    # Demo Requests
    path('demos/', views.demo_list, name='demo_list'),
    path('demos/<int:pk>/', views.demo_detail, name='demo_detail'),
    path('demos/<int:pk>/delete/', views.demo_delete, name='demo_delete'),

    # Contact Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),

    # Blog Posts
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # Features
    path('features/', views.feature_list, name='feature_list'),
    path('features/create/', views.feature_create, name='feature_create'),
    path('features/<int:pk>/edit/', views.feature_edit, name='feature_edit'),
    path('features/<int:pk>/delete/', views.feature_delete, name='feature_delete'),

    # Screenshots
    path('screenshots/', views.screenshot_list, name='screenshot_list'),
    path('screenshots/create/', views.screenshot_create, name='screenshot_create'),
    path('screenshots/<int:pk>/edit/', views.screenshot_edit, name='screenshot_edit'),
    path('screenshots/<int:pk>/delete/', views.screenshot_delete, name='screenshot_delete'),

    # Testimonials
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),

    # FAQs
    path('faqs/', views.faq_list, name='faq_list'),
    path('faqs/create/', views.faq_create, name='faq_create'),
    path('faqs/<int:pk>/edit/', views.faq_edit, name='faq_edit'),
    path('faqs/<int:pk>/delete/', views.faq_delete, name='faq_delete'),

    # Newsletter Subscribers
    path('subscribers/', views.subscriber_list, name='subscriber_list'),

    # Chat Conversations
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('chats/<int:pk>/delete/', views.chat_delete, name='chat_delete'),
]
