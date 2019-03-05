"""friends URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/chats/', views.Chats.as_view(), name='chats'),
    path('api/v1/chats/<int:id>/', views.ChatsId.as_view(), name='chat'),
    path('api/v1/colors/', views.Colors.as_view(), name='colors'),
    path('api/v1/rounds/', views.Rounds.as_view(), name='rounds'),
    path('api/v1/rounds/<int:round_id>/chats/', views.Chats.as_view(), name='chats-for-round'),
    path('api/v1/rounds/subscribe/', views.RoundsSubscribe.as_view(), name='rounds_subscribe'),
    path('api/v1/questions/', views.Questions.as_view(), name='questions'),
    path('api/v1/questions/answered/', views.QuestionsAnswered.as_view(), name='questions_answered'),
    path('api/v1/responses/', views.Responses.as_view(), name='responses'),
    path('api/v1/self/', views.Self.as_view(), name='self'),
    path('api/v1/feedback_questions/', views.FeedbackQuestions.as_view(), name='feedback_questions'),
    path('api/v1/chats/<int:id>/feedback_responses/', views.FeedbackResponses.as_view(), name='feedback_responses'),
    # For migrating Telegram users to Luminos
    path('api/v1/legacy/', views.Legacy.as_view(), name='legacy'),

    # Naming inspired by the Twilio tutorial API from https://github.com/TwilioDevEd/account-security-quickstart-django
    path('api/v1/verification/', views.Verification.as_view(), name='verification'),
    path('api/v1/verification/token/', views.VerificationToken.as_view(), name='verification_token'),
]
