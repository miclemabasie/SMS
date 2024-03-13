from django.shortcuts import render
from .models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile, Subject



def admin_dashboard(request):
    pass

    template_name = "staff/dashboard.html"
    context = {
        "section": "admin-area"
    }


    return render(request, template_name, context)


# Subjects

def list_all_subjects(request):
    subjects = Subject.objects.all()
    print(subjects)
    template_name = "subjects/subject-list.html"
    context = {
        "subjects": subjects,
    }

    return render(request, template_name, context)