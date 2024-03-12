from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.students.models import TeacherProfile, StudentProfile, Mark, Class 
from faker import Faker
from datetime import datetime, time, timezone


faker_factory = Faker()

User = get_user_model()


def teacher_list_view(request, *args, **kwargs):


    teachers = TeacherProfile.objects.all()

    template_name = "teachers/teachers-list.html"

    context = {
        "section": "teachers-area",
        "teachers": teachers
    }

    return render(request, template_name, context)


def teacher_detail_view(request, matricule, pkid, *args, **kwargs):
    teacher = get_object_or_404(TeacherProfile, matricule=matricule, pkid=pkid)
    template_name = "teachers/teacher-detail.html"
    context = {
        "section": "teachers-area",
        "teacher": teacher,
    }

    return render(request, template_name, context)

def teacher_edit_view(request, matricule, pkid, *args, **kwargs):
    teacher = get_object_or_404(TeacherProfile, matricule=matricule, pkid=pkid)

    if request.method == "POST":
        # Xtract data from the form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        subject = request.POST.get("subject")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        location = request.POST.get("location")
        country = request.POST.get("country")
        remark = request.POST.get("remark")
        username = request.POST.get("username")
        email = request.POST.get("email")
        profile_photo = request.FILES.get("photo")

        # Update user instance for the teacher
        

        teacher.user.username=username
        teacher.user.first_name=first_name
        teacher.user.last_name=last_name
        teacher.user.email=email
        
        teacher.user.save()

        
        # Update teacher profile instance

    
        teacher.gender = gender
        teacher.phone_number=phone
        teacher.main_subject = subject
        teacher.address = address

        teacher.save()
        if location:
            teacher.location = location
        if profile_photo:
            teacher.profile_photo = profile_photo
        if remark:
            teacher.remark = remark
        if country:
            teacher.country = country

        # construct a valid date out of the html date
        if dob:
            date_string_from_form = dob

            dob = datetime.strptime(date_string_from_form, '%Y-%m-%d').date()
            # Create a specific time
            specific_time = time(8, 51, 2)

            dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)
            teacher.user.dob=dob_with_time

        teacher.save()
        teacher.user.save()

        
        return redirect(reverse("teachers:teachers-detail", kwargs={"pkid": teacher.pkid, "matricule": teacher.matricule}))

    template_name = "teachers/teacher-edit.html"
    context = {
        "teacher": teacher,
        "section": "teachers-area"
    }

    return render(request, template_name, context)

def teacher_delete_view(request, matricule, pkid, *args, **kwargs):

    print("Deleting the user.")
    # template_name = "teachers/teacher-edit.html"
    context = {
        "section": "teachers-area"
    }

    return redirect(reverse("teachers:teachers-list"))


def teacher_add_view(request, *args, **kwargs):
    
    if request.method == "POST":
        # Xtract data from the form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        subject = request.POST.get("subject")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        location = request.POST.get("location")
        country = request.POST.get("country")
        remark = request.POST.get("remark")
        username = request.POST.get("username")
        email = request.POST.get("email")
        profile_photo = request.FILES.get("photo")

        # Create user instance for the teacher
        # construct a valid date out of the html date
        date_string_from_form = dob

        dob = datetime.strptime(date_string_from_form, '%Y-%m-%d').date()
        # Create a specific time
        specific_time = time(8, 51, 2)

        dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_teacher=True,
            dob=dob_with_time
        )
        user.save()
        user.set_password(faker_factory.password())
        user.save()

        # Create teacher profile instance

        teacher = TeacherProfile.objects.create(
            user=user,
            gender = gender,
            phone_number=phone,
            main_subject = subject,
            address = address,
        )
        teacher.save()
        if location:
            teacher.location = location
        if profile_photo:
            teacher.profile_photo = profile_photo
        if remark:
            teacher.remark = remark
        if country:
            teacher.country = country

        teacher.save()

        
        return redirect(reverse("teachers:teachers-detail", kwargs={"pkid": teacher.pkid, "matricule": teacher.matricule}))



    template_name = "teachers/teacher-add.html"
    context = {
        "section": "teachers-area"
    }

    return render(request, template_name, context)
