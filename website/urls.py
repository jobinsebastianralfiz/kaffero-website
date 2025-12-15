"""
URL patterns for Kaffero showcase website.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('features/', views.features, name='features'),
    path('features/<slug:slug>/', views.feature_detail, name='feature_detail'),
    path('pricing/', views.pricing, name='pricing'),
    path('demo/', views.demo, name='demo'),
    path('demo/thank-you/<int:pk>/', views.demo_thank_you, name='demo_thank_you'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Legal
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),

    # Actions
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Chatbot API
    path('api/chat/', views.chatbot_message, name='chatbot_message'),

    # SEO
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
