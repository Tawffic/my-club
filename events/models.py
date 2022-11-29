from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    zip_code =models.CharField(max_length=15)
    phone = models.CharField(max_length=25, blank= True)
    web = models.URLField("Website Address", blank=True)
    email_address = models.EmailField("Email Address", blank=True)


    def __str__(self):
        return self.name

class MyclubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField("Email Address")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Event(models.Model):
    name = models.CharField("Event Name", max_length=120)
    event_date = models.DateTimeField("Event Date")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,blank=True, null=True)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyclubUser, blank=True)


    def __str__(self):
        return self.name