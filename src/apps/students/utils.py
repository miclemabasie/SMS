from .models import StudentProfile, StudentTempCreateProfile, TeacherTempCreateProfile
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from apps.settings.models import Setting
from datetime import datetime, timezone
import random


def check_student_is_owing(student_pkid):
    student = StudentProfile.objects.get(pkid=student_pkid)
    if student.is_owing:
        return "Yes"
    else:
        return "No"


def check_student_is_repeater(student_pkid):
    student = StudentProfile.objects.get(pkid=student_pkid)
    if student.is_repeater:
        return "Yes"
    else:
        return "No"


def create_student_pin(student, pin):
    student_temp_profile, created = StudentTempCreateProfile.objects.get_or_create(
        pin=pin, email=student.user.email, student=student
    )
    if created:
        student_temp_profile.save()
        return True
    else:
        return False


def create_teacher_pin(teacher, pin):
    teacher_temp_profile, created = TeacherTempCreateProfile.objects.get_or_create(
        pin=pin, email=teacher.user.email, teacher=teacher
    )
    if created:
        teacher_temp_profile.save()

        return True
    else:
        return False


def get_student_temp_account(pin, email, student):
    student_pin = StudentTempCreateProfile.objects.filter(
        pin=pin, student=student, email=email
    )
    if student_pin.exists():
        pin = student_pin.first()
        return pin
    else:
        return False


def get_teacher_temp_account(pin, email, teacher):
    teacher_pin = TeacherTempCreateProfile.objects.filter(
        pin=pin, teacher=teacher, email=email
    )
    if teacher_pin.exists():
        pin = teacher_pin.first()
        return pin
    else:
        return False


# utils.py (or any appropriate module)


def send_password_reset_email(request, user, student_temp):
    school_setting = Setting.objects.all().first()

    # Generate a password reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Build the password reset URL
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = "https" if request.is_secure() else "http"
    reset_url = f"{protocol}://{domain}{reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    # Compose the email
    subject = f"Welcome to {school_setting.school_name} - Set Your Password"
    message = f"""
    Dear {user.first_name},

    Welcome to the f{school_setting.school_name}!

    To complete your account setup and set your password, please follow the link below:

    {reset_url}

    If you did not request this email, please ignore it.

    Best regards,
    {school_setting.school_name}
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)
    # delete the temp account
    student_temp.delete()


def send_account_creation_email(request, user):
    school_setting = Setting.objects.all().first()
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = "https" if request.is_secure() else "http"
    reset_url = f"{protocol}://{domain}{reverse('students:verify_pin')}"

    subject = f"Welcome to {school_setting.school_name}"
    message = f"""
    Dear {user.first_name},

    Welcome to the f{school_setting.school_name}!

    To complete your account setup and set your password, please follow the link below for identity check:

    {reset_url}

    If you did not request this email, please ignore it.

    Best regards,
    {school_setting.school_name}
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list)


def format_date(dob):
    # Process date of birth
    if isinstance(dob, datetime):
        # Ensure the datetime object has UTC timezone information
        if dob.tzinfo is None:
            dob = dob.replace(tzinfo=timezone.utc)
    elif isinstance(dob, str):
        # If dob is a string, parse it to a datetime object
        try:
            dob = datetime.strptime(dob, "%d-%m-%Y")  # Adjust format as necessary
            dob = dob.replace(tzinfo=timezone.utc)
            print("date when string", dob)
        except ValueError:
            print(f"Invalid date format for dob: {dob}")

    return dob


def generate_random_pin():
    random_strings = [str(random.randint(0, 9)) for _ in range(4)]

    pin = "".join(random_strings)
    return pin
