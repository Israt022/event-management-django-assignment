from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Event,User


@receiver(m2m_changed, sender=User.event.through)
def notify_participants_on_participant_creation(sender, instance, action, **kwargs):
    print("Print ",instance)
    if action == 'post_add':
        print(instance, instance.event.all())
        assigned_emails = [instance.email]
        print("Checking....", assigned_emails)

        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.event.first().name}",
            "esratjahangaming@gmail.com",
            assigned_emails,
            fail_silently=False,
        )
        