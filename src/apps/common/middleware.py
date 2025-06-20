# imports
# settings model
# redirect, reverse

from django.shortcuts import redirect
from django.urls import reverse
from apps.settings.models import Setting
from apps.terms.models import AcademicYear, Term


class CheckSetupMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # allow access to login page
        if request.path.startswith(reverse("users:user-login")):
            return self.get_response(request)

        # Allow access to the setup view to avoid enless redirects
        if request.path.startswith(reverse("settings:settings-home")):
            return self.get_response(request)

        # Allow access to the academic and term create routes
        if request.path.startswith(reverse("sessions:session-create")):
            return self.get_response(request)
        if request.path.startswith(reverse("sessions:term-create")):
            return self.get_response(request)

        if request.path.startswith(
            reverse("sessions:session-mark-active", kwargs={"pkid": 1})
        ):
            return self.get_response(request)

        if request.path.startswith(
            reverse("sessions:term-mark-active", kwargs={"pkid": 1})
        ):
            return self.get_response(request)
        # check if the settings have been initialized
        if not Setting.objects.exists():
            return redirect(reverse("settings:settings-home"))

        if not AcademicYear.objects.exists():
            return redirect(reverse("settings:setting-sessions"))
        if not AcademicYear.active_year_exists():
            return redirect(reverse("settings:setting-sessions"))

        if not Term.objects.exists():
            return redirect(reverse("settings:setting-terms"))
        if not Term.active_term_exists():
            return redirect(reverse("settings:setting-sessions"))

        response = self.get_response(request)
        return response
