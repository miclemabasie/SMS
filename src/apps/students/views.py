from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import StudentProfile, Class
from django.contrib.auth import get_user_model
from apps.profiles.models import ParentProfile
from datetime import datetime, timezone, time
import random


User = get_user_model()

from faker import Faker
faker = Faker()

def list_student_view(request):

    queryset = StudentProfile.objects.all()
    template_name = "students/list.html"
    context = {
        "section": "student-area",
        "students": queryset,
    }

    return render(request, template_name, context)


def student_detail_view(request, matricule, pkid):
    student = get_object_or_404(StudentProfile, matricule=matricule, pkid=pkid)

    template_name = "students/details.html"
    context = {
        "section": "student-area",
        "student": student
    }

    return render(request, template_name, context)


def add_student_view(request):
    classes = Class.objects.all()
    if request.method == "POST":
        print(request.POST)
        
        parent_fname = request.POST.get("first_name")
        parent_occupation = request.POST.get("parent-occupation")
        parent_phone = request.POST.get("parent-phone")
        parent_email = request.POST.get("parent-email")
        parent_address = request.POST.get("parent-address")
        parent_role = request.POST.get("parent-role")

        st_class = request.POST.get("student_class")
        # Get class in which student is part of
        student_class = get_object_or_404(Class, pkid=int(st_class))

        # Create parent for student
        student_parent = ParentProfile.objects.create(
            first_name=parent_fname,
            phone=parent_phone,
            occupation=parent_occupation,
            address=parent_address,
            email=parent_email,
            role=parent_role
        )

        student_parent.save()

        st_fname = request.POST.get("first_name")
        st_lname = request.POST.get("last_name")
        st_gender = request.POST.get("selected_gender")
        st_email = request.POST.get("email")
        st_dob = request.POST.get("dob")
        st_address = request.POST.get("address")
        st_phone = request.POST.get("phone")
        st_domain = request.POST.get("domain")
        st_image = request.FILES.get("profile_photo")

        # Create the user instance
        # construct a valid date out of the html date
        date_string_from_form = st_dob

        dob = datetime.strptime(date_string_from_form, '%Y-%m-%d').date()
        # Create a specific time
        specific_time = time(8, 51, 2)

        dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)

        # Construct faker usernames, this is done assuming that the usernames are not important to the students
        # we avoid using direct fake usernames, so as to avoid unique constrainst failure in the database
        # This is why the random digit is added to the end of every fake username generated by faker
        faker_username = faker.user_name()
        # attache random digit to the end
        faker_username + str(random.randint(0,9))

        if not st_email:
            st_email = faker.email()
 
        user = User.objects.create(
            username=faker_username,
            first_name=st_fname,
            last_name=st_lname,
            email=st_email,
            is_student=True,
            dob=dob_with_time
        )

        user.save()


        # Create student instance

        student = StudentProfile.objects.create(
            user = user,
            parent = student_parent,
            current_class=student_class,
            gender = st_gender,
            phone_number=st_phone,
            # profile_photo=st_photo,
            address = st_address,
            domain = st_domain,
        )

        student.save()
        if st_image:
            student.profile_photo = st_image
        student.save()
        return redirect(reverse("students:student-list"))

        
    else:
        pass
    template_name = "students/add.html"

    context = {
        "section": "student-area",
        "classes": classes
    }

    return render(request, template_name, context)


def edit_student_profile(request, pkid, matricule):
    student = get_object_or_404(StudentProfile, pkid=pkid, matricule=matricule)

    if request.method == "POST":
        st_class = request.POST.get("student_class")
        student_class = get_object_or_404(Class, pkid=int(st_class))

        st_fname = request.POST.get("first_name")
        st_lname = request.POST.get("last_name")
        st_gender = request.POST.get("selected_gender")
        st_email = request.POST.get("email")
        st_dob = request.POST.get("dob")
        st_address = request.POST.get("address")
        st_phone = request.POST.get("phone")
        st_domain = request.POST.get("domain")
        st_image = request.FILES.get("profile_photo")

        print("This is the image", st_image)

        # Parse date string from form
        dob = datetime.strptime(st_dob, '%Y-%m-%d').date()
        specific_time = time(8, 51, 2)

        dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)

        # Update user fields
        student.user.first_name = st_fname
        student.user.last_name = st_lname
        student.user.email = st_email
        student.user.dob = dob_with_time

        if st_image:
            student.profile_photo = st_image
        student.user.save()

        # Update student fields
        student.current_class = student_class
        student.gender = st_gender
        student.phone_number = st_phone
        student.address = st_address
        student.domain = st_domain

        student.save()
        return redirect(reverse("students:student-detail", kwargs={"pkid": student.pkid, "matricule": student.matricule}))

    # Get and associate a parent to the request.
    parent = student.parent
    template_name = "students/edit.html"
    context = {
        "section": "student_area",
        'student_profile': student,
        'dob': str(student.user.dob.date()),
        "classes": Class.objects.all()
    }

    return render(request, template_name, context)