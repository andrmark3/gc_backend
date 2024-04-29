from django.db import models

class Event(models.Model):
    # Normal Fields
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField(max_length=1000)
    
    # Boolean Fild
    is_published = models.BooleanField(default=True)

    # Date Fields
    published_date = models.DateField('date published the event will be published in the FE')
    launch_date = models.DateField('data the event is officil launched')
    register_start_date = models.DateField('date event registration starts')
    register_end_date = models.DateField('date event registration ends')

    # Media Fields
    image = models.ImageField(upload_to='.event_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Participant(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    phone = models.IntegerField(null=False)

    def __str__(self):
        return (self.first_name + self.last_name)