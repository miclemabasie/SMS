from django.shortcuts import render, redirect
from django.urls import reverse
from apps.terms.models import ExaminationSession, Term, AcademicYear
from .models import Setting
from django.contrib import messages
from django.contrib.auth.models import Group, Permission


def settings_view(request):

    if request.method == "POST":
        # initialize a new setting object
        # Check if setting already exist in the database
        setting = Setting.objects.filter()
        if setting.exists():
            messages.error(request, "Settings already initialized.")
            return redirect(reverse("settings:settings-home"))

        setting = Setting.objects.create()
        setting.save()

        # Create the different groups needed to run the system
        students_group, created = Group.objects.get_or_create(name="students")
        teachers_group, created = Group.objects.get_or_create(name="teachers")
        admin_group, created = Group.objects.get_or_create(name="administrator")

        # Define the permissions to add (adjust these to fit your needs)
        student_permissions = [
            "change_studentprofile",
            "change_class",
            "view_subject",
            "view_reportcard",
            "view_studentprofile",
        ]

        teacher_permissions = []

        # Add student_permissions to the group
        for perm in student_permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                students_group.permissions.add(permission)
                message += f'Permission "{perm}" added to group "students".\n'
            except Permission.DoesNotExist:
                message += f'Permission "{perm}" does not exist.\n'

        messages.success(request, "Setting have been successfully initialized.")
        return redirect(reverse("settings:settings-home"))

    setting = Setting.objects.all().first()

    template_name = "settings/settings.html"
    context = {"section": "settings", "setting": setting}

    return render(request, template_name, context)


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group, Permission


def create_student_group(request):
    # Create the students group
    group, created = Group.objects.get_or_create(name="students")

    if created:
        message = 'Group "students" created successfully.\n'
    else:
        message = 'Group "students" already exists.\n'

    # Define the permissions to add (adjust these to fit your needs)
    permissions = [
        "add_mymodel",
        "change_mymodel",
        "delete_mymodel",
        "view_mymodel",
    ]

    # Add permissions to the group
    for perm in permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)
            message += f'Permission "{perm}" added to group "students".\n'
        except Permission.DoesNotExist:
            message += f'Permission "{perm}" does not exist.\n'

    return HttpResponse(message, content_type="text/plain")


def update_settings(request):
    settings = Setting.objects.all()
    if len(settings) > 0:
        setting = settings.first()
    else:
        messages.error(request, "Settings have not yet been initialized.")
        return redirect(reverse("settings:settings-home"))

    if request.method == "POST":
        # extract the fields
        data = request.POST
        school_name = data.get("school_name")
        currency = data.get("currency")
        country = data.get("country")
        city = data.get("city")
        address1 = data.get("address1")
        address2 = data.get("address2")
        postal = data.get("postal")
        motto = data.get("motto")
        logo = request.FILES.get("logo")
        favicon = request.FILES.get("favicon")

        print(logo)

        setting.school_name = school_name
        if currency:
            setting.currency = currency
        if country:
            setting.country = country
        if city:
            setting.city = city
        if address1:
            setting.address1 = address1
        if address2:
            setting.address2 = address2
        if postal:
            setting.postal_code = postal
        if motto:
            setting.motto = motto

        if logo:
            print("This is the logo", logo)
            setting.school_logo = logo
        if favicon:
            setting.school_favicon = favicon

        setting.save()

        messages.success(request, "Settings have been successfully updated")

        return redirect(reverse("settings:settings-home"))
    return redirect(reverse("settings:settings-home"))


def session_settings_view(request):

    sessions = AcademicYear.objects.all()
    current_session = sessions.filter(is_current=True).first()
    template_name = "settings/session-settings.html"
    context = {
        "section": "settings",
        "sessions": sessions,
        "current_session": current_session,
    }

    return render(request, template_name, context)


def term_settings_view(request):

    sessions = AcademicYear.objects.all()
    terms = Term.objects.all()

    current_session = sessions.filter(is_current=True).first()
    current_term = terms.filter(is_current=True).first()
    template_name = "settings/term-settings.html"
    context = {
        "section": "settings",
        "sessions": sessions,
        "terms": terms,
        "current_session": current_session,
        "current_term": current_term,
    }

    return render(request, template_name, context)


def exam_session_view(request):

    exam_sessions = ExaminationSession.objects.all()
    sessions = AcademicYear.objects.all()
    terms = Term.objects.all()

    current_session = sessions.filter(is_current=True).first()
    current_term = terms.filter(is_current=True).first()
    current_exam_session = ExaminationSession.objects.filter(is_current=True).first()

    template_name = "settings/exam-session.html"
    context = {
        "section": "settings",
        "sessions": sessions,
        "terms": terms,
        "exam_sessions": exam_sessions,
        "current_session": current_session,
        "current_term": current_term,
        "current_exam_session": current_exam_session,
    }

    return render(request, template_name, context)


# To be done later
def add_class_pass_avg(request):
    pass
