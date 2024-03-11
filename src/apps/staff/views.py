from django.shortcuts import render
from .models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile



def admin_dashboard(request):
    pass

    template_name = "staff/dashboard.html"
    context = {
        "section": "admin-area"
    }


    return render(request, template_name, context)