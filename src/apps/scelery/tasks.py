from django.core.mail import send_mail
from time import sleep
from celery import shared_task, Celery
from django.core.mail import EmailMultiAlternatives

app = Celery("sms")


@shared_task(bind=True)
def send_feedback_mail(
    self, subject, message, from_email, recipient_list, html_content=None
):
    email_message = EmailMultiAlternatives(subject, message, from_email, recipient_list)
    print(email_message)
    if html_content:
        email_message.attach_alternative(html_content, "text/html")
    print("Sending mail")
    email_message.send()
