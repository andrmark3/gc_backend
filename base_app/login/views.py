import os
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .models import CustomToken
from .serializers import UserSerializer

TOKEN_EXP = int(os.getenv('TOKEN_EXPIRATION_TIME'))


class CustomAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Check if user already has a token
        try:
            token = CustomToken.objects.get(user=user)
        except CustomToken.DoesNotExist:
            token = None

        # If token exists and not expired, return existing token
        # if token and not token.is_expired():
        #     return Response({'token': token.key})

        # If token exists but expired, delete it
        if token and token.is_expired():
            token.delete()

        if token == None:
            # Generate a new token with expiration time 
            expiration = datetime.now() + timedelta(minutes=TOKEN_EXP)
            token = CustomToken.objects.create(user=user, expiration=expiration)
            token.save()
        
        user_serializer = UserSerializer(user)
        response_data = user_serializer.data
        del response_data['password']
        response_data['token'] = token.key
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Customize the email content based on your requirements
            subject = 'Participant Registration Confirmation'
            email_template = 'welcome_new_user.html'

            context = {
                'username': serializer.data['username'],
            }

            # Render the HTML content using the template and context
            message = render_to_string(email_template, context)

            # Set the sender and recipient emails
            from_email = 'group_consulter_demo@androvice.gr'
            recipient_list = [serializer.data['email']]

            # Send the email
            send_mail(subject, message, from_email, recipient_list, html_message=message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            response_data = serializer.data
            del response_data['password']
            return Response(response_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
