''' imports of celary shaered task, send mail function and setting sto get mail'''
from celery import shared_task
from django.core.mail import send_mail
from blog22 import settings



@shared_task
def sent_mail2(msg, email):
    '''task to sent mail when coment is made'''
    send_mail(
        subject="Alert  mail",
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
            )
    return f"mail sent{email}"




@shared_task
def test(msg, email):
    '''task to test celary'''
    print(msg, email)
    return "Done"
