from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import time
from django.contrib import messages
from apps.scelery.tasks import send_feedback_mail

# Create your views here.


def form_view(request):

    if request.method == "POST":
        # get the name and message from the form
        email = request.POST.get("email")
        message = request.POST.get("message")
        # send a message to the user
        subject = "Application for Internship"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = "test@mail.com"
        send_feedback_mail.delay(subject, message, from_email, recipient_list)
        messages.success(request, "Success!")
        return redirect(reverse("form"))

    template_name = "form.html"
    context = {"title": "Testing out celery."}

    return render(request, template_name, context)
