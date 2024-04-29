import base64
import qrcode
from io import BytesIO

from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Event, Participant
from .serializers import EventSerializer, ParticipantSerializer



class EventViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_queryset(self):
        # Get the queryset of all events
        queryset = Event.objects.all()

        # Filter out events where the published_date is less than or equal to today's date
        queryset = queryset.filter(published_date__lte=timezone.now(), is_published=True)

        return queryset
    
    
class ParticipantViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    
    def perform_create(self, serializer):
        # Call the parent method to save the participant object
        instance = serializer.save()

        # Customize the email content based on your requirements
        subject = 'Participant Registration Confirmation'
        email_template = 'event_registration_email.html'

        context = {
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'event_title': instance.event_id.title,
            'register_start_date': instance.event_id.register_start_date
        }

        # Render the HTML content using the template and context
        message = render_to_string(email_template, context)

        # Set the sender and recipient emails
        from_email = 'group_consulter_demo@androvice.gr'
        recipient_list = [instance.email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list, html_message=message)

        # Return a response indicating the successful creation
        return Response(serializer.data, status=status.HTTP_201_CREATED)



def send_email_with_qr(request):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("https://www.google.com")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert QR code image to base64
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Render HTML template with QR code image embedded
    context = {
        'qr_code_image': qr_img_base64,
        'qr_code_alt_text': 'QR Code',
    }
    html_content = render_to_string('email_template_with_qr.html', context)
    text_content = strip_tags(html_content)

    # Send email with HTML content
    subject = 'Welcome to Our Website'
    from_email = 'group_consulter_demo@androvice.gr'
    to_email = ['and.markou@outlook.com']
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse('Email sent successfully!')
