import os
from django.http import JsonResponse
from django.utils import timezone
from .models import CustomToken

TOKEN_EXP = int(os.getenv('TOKEN_EXPIRATION_TIME'))



class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract token from request headers
        authorization_header = request.headers.get('Authorization')

        if authorization_header and authorization_header.startswith('Token '):
            token_key = authorization_header.split(' ')[1]

            try:
                token = CustomToken.objects.get(key=token_key)

                # Convert current time to offset-aware datetime
                current_time = timezone.now()

                # Check if the token has expired
                if token.expiration < current_time:
                    return JsonResponse({'error': 'Token has expired'}, status=401)

                # Attach user object to request for authentication
                request.user = token.user

            except CustomToken.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)

        return self.get_response(request)
