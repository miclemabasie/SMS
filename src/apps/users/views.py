from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout


def login_view(request):


    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password = password)
        if user:
            login(request, user=user)

            # Check user type and redirect to proper page
            if user.is_admin:
                return redirect("staff:admin-dashboard")
            if user.is_teacher:
                pass
            if user.is_student:
                pass
            return redirect("staff:admin-dashboard")

    template_name = "accounts/login.html"

    form = LoginForm()

    context = {
        "section": "accounts",
        "form": form,
    }

    return render(request, template_name, context)


def logout_view(request):
    logout(request)

    return redirect("users:user-login")
