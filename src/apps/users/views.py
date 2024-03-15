from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def login_view(request):


    if request.method == "POST":

        form = LoginForm(request.POST)
        # validate login activity

        print(form)


    template_name = "accounts/login.html"

    form = LoginForm()

    context = {
        "section": "accounts",
        "form": form,
    }

    return render(request, template_name, context)