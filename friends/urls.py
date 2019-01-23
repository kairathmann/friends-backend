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
    path('api/v1/self/', views.Self.as_view(), name='self'),
    path('api/v1/self/responses/', views.SelfResponses.as_view(), name='self_responses'),
    path('api/v1/self/questions/', views.SelfQuestions.as_view(), name='self_questions'),

    # Naming inspired by the Twilio tutorial API from https://github.com/TwilioDevEd/account-security-quickstart-django
    path('api/v1/verification/', views.Verification.as_view(), name='verification'),
    path('api/v1/verification/token/', views.VerificationToken.as_view(), name='verification_token'),
]
