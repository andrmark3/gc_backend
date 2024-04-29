from django.utils import timezone
from django.db import models
from rest_framework.authtoken.models import Token

class CustomToken(Token):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey('auth.User', related_name='custom_tokens', on_delete=models.CASCADE)
    expiration = models.DateTimeField()

    def is_expired(self):
        return self.expiration < timezone.now()

    def __str__(self):
        return self.key
    

