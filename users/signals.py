from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(post_save,sender=User)
def activation_email(sender,instance,created,**kwargs):
    # Debugging prints
    print("=== DEBUG EMAIL SETTINGS ===")
    print("EMAIL_HOST:", settings.EMAIL_HOST)
    print("EMAIL_PORT:", settings.EMAIL_PORT)
    print("EMAIL_USE_TLS:", settings.EMAIL_USE_TLS)
    print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
    print("FRONTEND_URL:", settings.FRONTEND_URL)
    print("User created:", created)
    print("User email:", instance.email)
    print("============================")
    # if created:
    #     token = default_token_generator.make_token(instance)
    #     activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
    #     subject = 'Activate Your Account'
    #     message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
    #     recipient_list = [instance.email]
        
    #     try:
    #         send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
    #     except Exception as e:
    #         print(f'Failed to send email to {instance.email} : {str(e)}')
    print("sending activation email")
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        mail_subject ='Activate Your user account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
        recipient_list = [instance.email]
        try:
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER,recipient_list)
            print("email sended")
        
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")   
            
@receiver(post_save,sender = User)
def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name = 'User')
        instance.groups.add(user_group)
        # instance.save()

        
        