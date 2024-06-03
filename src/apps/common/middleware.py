# imports
# settings model
# redirect, reverse

from django.shortcuts import redirect
from django.urls import reverse
from apps.settings.models import Setting


class CheckSetupMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to the setup view to avoid enless redirects
        if request.path.startswith(reverse("settings:settings-home")):
            return self.get_response(request)

        # check if the settings have been initialized
        if not Setting.objects.exists():
            return redirect(reverse("settings:settings-home"))

        response = self.get_response(request)
        return response
