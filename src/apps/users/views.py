from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm


def login_view(request):
    remember_me = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = request.POST.get("remember_me") == "yes"

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user=user)

                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser close

                if user.is_student:
                    return redirect(reverse("students:student-dashboard"))
                if user.is_teacher:
                    return redirect(reverse("teachers:teacher-dashboard"))
                if user.is_admin:
                    return redirect(reverse("staff:admin-dashboard"))
            else:
                form.add_error(None, "Invalid email or password")
        # If form is not valid, it will be passed back with errors
    else:
        form = LoginForm()

    template_name = "accounts/login.html"
    context = {
        "section": "accounts",
        "form": form,
    }
    return render(request, template_name, context)


def logout_view(request):
    logout(request)

    return redirect("users:user-login")
