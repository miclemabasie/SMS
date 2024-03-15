from django.shortcuts import render, get_object_or_404
from .models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile, Subject, Class
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


@login_required
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

def assign_subject_to_classes(request, pkid):
    subjects = Subject.objects.all()
    klass = get_object_or_404(Class, pkid=pkid)

    selected_subjects = klass.subjects.all()

    unselected_subjects = []    
    for subject in subjects:
        if subject not in selected_subjects:
            unselected_subjects.append(subject)

    if request.method == "POST":
        selected_subjects = request.POST.getlist("selectedSubjects")


        print("This are the selected subjects", request.body)
        data = json.loads(request.body)

        selected_subjects_ids = []
        for subject in data["selectedSubjects"]:
            print(subject["pkid"])
            selected_subjects_ids.append(subject.get("pkid"))
        
        print(selected_subjects_ids)

        return JsonResponse({"message": "updated."})

    template_name = "subjects/subject-assign.html"

    context = {
        "section": "subjects",
        "class": klass,
        "unselected_subjects": unselected_subjects,
        "selected_subjects": selected_subjects
    }

    return render(request, template_name, context)