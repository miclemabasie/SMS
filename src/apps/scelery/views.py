from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from apps.scelery.tasks import send_feedback_mail


def form_view(request):
    if request.method == "POST":
        # get the name and message from the form
        email = request.POST.get("email")
        name = request.POST.get("name")

        # send a message to the user
        subject = "Welcome to Grader!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        # render the HTML email template with context
        context = {"name": name}
        html_content = render_to_string("emails/testing.html", context)

        # call the Celery task
        send_feedback_mail.delay(subject, "", from_email, recipient_list, html_content)

        messages.success(request, "Success!")
        return redirect(reverse("form"))

    template_name = "form.html"
    context = {"title": "Testing out celery."}
    return render(request, template_name, context)
