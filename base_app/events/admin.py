from django.contrib import admin
from .models import Event, Participant

class ParticipantAdmin(admin.ModelAdmin):        
    list_display = ('first_name','last_name','email','phone')
    list_filter = ('event_id',) #for filtering


admin.site.register(Event)
admin.site.register(Participant, ParticipantAdmin)