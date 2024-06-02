from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile, Subject, Class
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def admin_dashboard(request):
    pass

    template_name = "staff/dashboard.html"
    context = {"section": "admin-area"}

    return render(request, template_name, context)


# Subjects
@login_required
def list_all_subjects(request):
    subjects = Subject.objects.all()
    print(subjects)
    template_name = "subjects/subject-list.html"
    context = {
        "subjects": subjects,
    }

    return render(request, template_name, context)


@login_required
def delete_subject(request, pkid, *args, **kwargs):
    subject = get_object_or_404(Subject, pkid=pkid)

    subject.delete()

    return redirect(reverse("staff:subjects"))


@login_required
def add_subject_view(request, *args, **kwargs):
    if request.method == "POST":
        # Extract form data
        subject_name = request.POST.get("subject_name")
        subject_code = request.POST.get("subject_code")
        subject_coeff = request.POST.get("subject_coeff")

        # Create a subject instance
        subject = Subject.objects.create(
            name=subject_name, code=subject_code, coef=subject_coeff
        )
        subject.save()
        messages.success(request, "Subject added.")

        return redirect(reverse("staff:subjects"))
    return redirect(reverse("staff:subjects"))


@login_required
def edit_subject_view(request, pkid, *args, **kwargs):
    subject = get_object_or_404(Subject, pkid=pkid)
    if request.method == "POST":
        # Extract form data
        subject_name = request.POST.get("subject_name")
        subject_code = request.POST.get("subject_code")
        subject_coeff = request.POST.get("subject_coeff")

        # Update subject instance
        subject.name = subject_name
        subject.code = subject_code
        subject.coef = subject_coeff

        subject.save()
        messages.success(request, "Subject Updated succesfully.")

        return redirect(reverse("staff:subjects"))
    return redirect(reverse("staff:subjects"))


@login_required
def assign_subject_to_classes(request, pkid):
    subjects = Subject.objects.all()
    klass = get_object_or_404(Class, pkid=pkid)

    selected_subjects = klass.subjects.all()

    unselected_subjects = []
    for subject in subjects:
        if subject not in selected_subjects:
            unselected_subjects.append(subject)

    if request.method == "POST":
        print("This are the selected subjects", request.body)
        data = json.loads(request.body)

        selected_subjects_ids = []
        for subject in data["selectedSubjects"]:
            print(subject["pkid"])
            selected_subjects_ids.append(subject.get("pkid"))
        print(selected_subjects_ids)
        # Flush out all the subjects that exist in the class and reset
        print(
            "we are inside the loop", len(selected_subjects), len(selected_subjects_ids)
        )
        if len(selected_subjects) > 0 and len(selected_subjects_ids) > 0:
            for subject in selected_subjects:
                print("This is the subject", subject)
                klass.subjects.remove(subject)
                klass.save()

        print(klass.subjects.all())

        # Reassign the subjects to the klass instance
        # Ge throught the incoming ids, and get the subjects associated the with the pkids
        for pkid in selected_subjects_ids:
            sub = Subject.objects.filter(pkid=pkid).first()
            if sub:
                klass.subjects.add(sub)
                klass.save()

        return JsonResponse({"message": "updated."})

    template_name = "subjects/subject-assign.html"

    context = {
        "section": "subjects",
        "class": klass,
        "unselected_subjects": unselected_subjects,
        "selected_subjects": selected_subjects,
    }

    return render(request, template_name, context)


@login_required
def create_staff(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # subject = request.POST.get("subject")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        location = request.POST.get("location")
        country = request.POST.get("country")
        photo = request.FILES.get("photo")
        # pin = request.POST.get("pin")
        remark = request.POST.get("remark")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("selected_role")

        # Permissions
        generate_reports = request.POST.get("generate_reports") == "on"
        manage_students = request.POST.get("manage_students") == "on"
        manage_teachers = request.POST.get("manage_teachers") == "on"
        manage_admins = request.POST.get("manage_admins") == "on"
        manage_sessions = request.POST.get("manage_sessions") == "on"
        manage_subjects = request.POST.get("manage_subjects") == "on"

        print(
            "This are different permissions",
            generate_reports,
            manage_students,
            manage_teachers,
            manage_admins,
            manage_sessions,
            manage_subjects,
        )

        # Create User object
        user = User.objects.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            dob=dob,
        )

        user.is_admin = True
        user.save()

        # Create AdminProfile object

        admin_profile = AdminProfile(
            user=user,
            gender=gender,
            phone_number=phone,
            profile_photo=photo,
            country=country,
            location=location,
            address=address,
            role=role,
            remark=remark,
            generate_reports=generate_reports,
            manage_students=manage_students,
            manage_teachers=manage_teachers,
            manage_admins=manage_admins,
            manage_sessions=manage_sessions,
            manage_subjects=manage_subjects,
        )
        admin_profile.save()

    template_name = "staff/create-admin.html"
    context = {
        "section": "admin",
    }

    return render(request, template_name, context)


@login_required
def list_admin(request):
    # get all the admins from the system

    admins = AdminProfile.objects.all()

    template_name = "staff/list-admin.html"

    context = {
        "admins": admins,
    }

    return render(request, template_name, context)
