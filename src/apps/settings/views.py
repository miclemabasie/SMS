from django.shortcuts import render, redirect
from django.urls import reverse
from apps.terms.models import ExaminationSession, Term, AcademicYear
from .models import Setting
from django.contrib import messages


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
        messages.success(request, "Setting have been successfully initialized.")
        return redirect(reverse("settings:settings-home"))

    setting = Setting.objects.all().first()

    template_name = "settings/settings.html"
    context = {"section": "settings", "setting": setting}

    return render(request, template_name, context)


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
