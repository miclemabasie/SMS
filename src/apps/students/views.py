from django.shortcuts import render
from .models import StudentProfile


def list_student_view(request):
    queryset = StudentProfile.objects.all()


    template_name = "students/list.html"
    context = {
        "students": queryset,
    }

    return render(request, template_name, context)