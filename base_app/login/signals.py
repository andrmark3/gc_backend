import os
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import CustomToken
from datetime import timedelta

TOKEN_EXP = int(os.getenv('TOKEN_EXPIRATION_TIME'))

@receiver(user_logged_in)
def generate_token_with_expiration(sender, user, request, **kwargs):
    token, created = CustomToken.objects.get_or_create(user=user)
    if created or token.is_expired():
        token.expiration = token.created + timedelta(minutes=TOKEN_EXP)
        token.save()
