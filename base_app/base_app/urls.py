"""
URL configuration for base_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from login.views import CustomAuthTokenView
from events.views import ParticipantViewSet, EventViewSet, send_email_with_qr
from login.views import UserRegistrationView, UserUpdateView


router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path("admin/", admin.site.urls),
    
    # User APIS
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('user_update/', UserUpdateView.as_view(), name='user-update'),
    path('api-token-auth/', CustomAuthTokenView.as_view(), name='api_token_auth'),
    
    # QR EMAIL GENERATOR
    path("qr_email", send_email_with_qr, name="test_email_csend_email_with_qronnection"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


