from django.contrib import admin
from .models import CustomToken

class CustomTokenAdmin(admin.ModelAdmin):        
    list_display = ('key','user','expiration')

admin.site.register(CustomToken, CustomTokenAdmin)

