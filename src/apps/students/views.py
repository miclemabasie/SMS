from django.shortcuts import render, get_object_or_404
from .models import StudentProfile
from django.contrib.auth.models import User


def list_student_view(request):
    queryset = StudentProfile.objects.all()


    template_name = "students/list.html"
    context = {
        "students": queryset,
    }

    return render(request, template_name, context)


def student_detail_view(request, matricule, pkid):
    student = get_object_or_404(StudentProfile, matricule=matricule, pkid=pkid)

    template_name = "students/details.html"
    context = {
        "student": student
    }

    return render(request, template_name, context)