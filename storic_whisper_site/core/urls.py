from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # MAIN PAGES
    path('women-psychology/', views.women, name='women'),
    path('stoicism/', views.stoicism, name='stoicism'),
    path('breakup/', views.breakup, name='breakup'),
    path('about/', views.about, name='about'),
    path('dark-psychology/', views.dark_psychology, name='dark'),

    # PSYCHOLOGY PILLARS
    path('dopamine/', views.dopamine, name='dopamine'),
    path('human-behavior/', views.human_behavior, name='human_behavior'),
    path('self-transformation/', views.self_transform, name='self_transform'),
    path('ai-mind/', views.ai_mind, name='ai_mind'),

    # LUPPI AI
    path('ai-saathi/', views.ai_assistant, name='ai_assistant'),
    path('ai-saathi/chat/', views.luppi_chat_api, name='luppi_chat'),

    # NEWSLETTER
    path('subscribe/', views.subscribe, name='subscribe'),

    # LEGAL PAGES
    path('privacy-policy/', views.privacy, name='privacy'),
    path('terms-and-conditions/', views.terms, name='terms'),

    # ENGLISH GLOBAL HUB
    path('en/', views.english_hub, name='english_hub'),

    # ARTICLES / BLOG
    path('articles/', views.article_list, name='article_list'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),

]