from django.shortcuts import render
from apps.terms.models import ExaminationSession, Term, AcademicYear


def settings_view(request):
    template_name = "settings/settings.html"
    context = {
        "section": "settings"
    }


    return render(request, template_name, context)


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

    