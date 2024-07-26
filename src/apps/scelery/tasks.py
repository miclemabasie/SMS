from django.core.mail import send_mail
from time import sleep
from celery import shared_task, Celery


app = Celery("sms")


@shared_task(bind=True)
def send_feedback_mail(self, subject, message, sender, email, *args, **kwargs):
    sleep(20)
    send_mail(subject, message, sender, [email])
