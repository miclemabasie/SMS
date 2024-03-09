from django.shortcuts import render
from .models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile



def admin_dashboard(request):
    pass

    template_name = ""
    context = {}
    return render(request, template_name, context)