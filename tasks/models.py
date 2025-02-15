from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save, m2m_changed
from django.core.mail import send_mail

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey("Category",  on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Participant(models.Model):
    name = models.CharField(max_length=250)
    email= models.EmailField(unique=True)
    event = models.ManyToManyField(Event,related_name='event')
    
    def __str__(self):
        return self.name

@receiver(m2m_changed, sender=Participant.event.through)
def notyfy(sender,instance,action, **kwargs):
    if action == 'post_add':
        assigned_emails = [par.email for par in instance.event.all()]
        print("Assigned emails:", assigned_emails)
        send_mail(
            "New Participant Assigned",
            f"You have been Joined to the Event : {instance.event}",
            "esratjahangaming@gmail.com",
            assigned_emails,
            fail_silent = False,
        )

