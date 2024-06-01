from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.announcements.models import Announcement, Event
from apps.fees.models import Fee
from apps.students.forms import VerifyPinForm
from apps.students.models import (
    TeacherProfile,
    StudentProfile,
    Mark,
    Class,
    TeacherTempCreateProfile,
)
from faker import Faker
from datetime import datetime, time, timezone
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from openpyxl import workbook, load_workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from apps.students.utils import (
    get_student_temp_account,
    get_teacher_temp_account,
    send_account_creation_email,
    generate_random_pin,
    create_teacher_pin,
    send_password_reset_email,
)
from apps.terms.models import AcademicYear, ExaminationSession, Term

faker_factory = Faker()

User = get_user_model()


@login_required
def teacher_list_view(request, *args, **kwargs):

    teachers = TeacherProfile.objects.all()

    template_name = "teachers/teachers-list.html"

    context = {"section": "teachers-area", "teachers": teachers}

    return render(request, template_name, context)


@login_required
def teacher_detail_view(request, matricule, pkid, *args, **kwargs):
    teacher = get_object_or_404(TeacherProfile, matricule=matricule, pkid=pkid)
    template_name = "teachers/teacher-detail.html"
    pin = TeacherTempCreateProfile.objects.filter(teacher=teacher)
    if pin.exists():
        pin = pin.first()
    else:
        pin = None
    context = {
        "section": "teachers-area",
        "teacher": teacher,
        "pin": pin,
    }

    return render(request, template_name, context)


@login_required
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

        teacher.user.username = username
        teacher.user.first_name = first_name
        teacher.user.last_name = last_name
        teacher.user.email = email

        teacher.user.save()

        # Update teacher profile instance

        teacher.gender = gender
        teacher.phone_number = phone
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

            dob = datetime.strptime(date_string_from_form, "%Y-%m-%d").date()
            # Create a specific time
            specific_time = time(8, 51, 2)

            dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)
            teacher.user.dob = dob_with_time

        teacher.save()
        teacher.user.save()

        messages.success(request, "TEacher successfully updated")

        return redirect(
            reverse(
                "teachers:teachers-detail",
                kwargs={"pkid": teacher.pkid, "matricule": teacher.matricule},
            )
        )

    template_name = "teachers/teacher-edit.html"
    context = {"teacher": teacher, "section": "teachers-area"}

    return render(request, template_name, context)


@login_required
def teacher_delete_view(request, matricule, pkid, *args, **kwargs):

    teacher = get_object_or_404(TeacherProfile, matricule=matricule, pkid=pkid)

    print("Deleting the user.")

    teacher.delete()

    messages.success(request, "Teacher successfuly deleted.")

    # template_name = "teachers/teacher-edit.html"

    return redirect(reverse("teachers:teachers-list"))


@login_required
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
        pin = request.POST.get("pin")

        if len(pin) == 4:
            # create temp
            pass
        else:
            messages.error(
                "Password reset pin has incorrect length, should be exactly 4."
            )
            return redirect(reverse("teachers:teachers-add"))

        # Create user instance for the teacher
        # construct a valid date out of the html date
        date_string_from_form = dob

        dob = datetime.strptime(date_string_from_form, "%Y-%m-%d").date()
        # Create a specific time
        specific_time = time(8, 51, 2)

        dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_teacher=True,
            dob=dob_with_time,
        )
        user.save()
        user.set_password(faker_factory.password())
        user.save()

        # Create teacher profile instance

        teacher, created = TeacherProfile.objects.get_or_create(
            user=user,
            gender=gender,
            phone_number=phone,
            main_subject=subject,
            address=address,
        )
        if created:
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
            teacher.user.is_teacher = True
            create_teacher_pin(teacher, pin)
            send_account_creation_email(request, teacher.user, "teacher")
            return redirect(
                reverse(
                    "teachers:teachers-detail",
                    kwargs={"pkid": teacher.pkid, "matricule": teacher.matricule},
                )
            )
        else:
            messages.warning(request, "Teacher already exist.")
            return redirect(reverse("teachers:teachers-list"))

    template_name = "teachers/teacher-add.html"
    context = {"section": "teachers-area"}

    return render(request, template_name, context)


@login_required
def class_add_view(request, *args, **kwargs):

    if request.method == "POST":

        # extract information from the class form
        grade_level = request.POST.get("grade_level")
        class_name = request.POST.get("class_name")
        class_master = request.POST.get("class_master")
        class_prefect = request.POST.get("class_prefect")

        print(class_prefect, class_master)

        # Create the class
        if grade_level and class_name:

            klass = Class.objects.create(
                grade_level=grade_level,
                class_name=class_name,
                class_master=class_master,
                class_prefect=class_prefect,
            )

            klass.save()
        save_and_add_flag = request.POST.get("save_and_add")

        if save_and_add_flag:
            print(save_and_add_flag)
            return redirect(reverse("class-add"))
        return redirect(reverse("class-list"))

    template_name = "classes/class-add.html"
    context = {"section": "class-area"}

    return render(request, template_name, context)


@login_required
def class_list_view(request, *args, **kwargs):

    classes = Class.objects.all()

    template_name = "classes/class-list.html"
    context = {
        "section": "class-area",
        "classes": classes,
    }

    return render(request, template_name, context)


@login_required
def class_edit_view(request, pkid, *args, **kwargs):

    klass = get_object_or_404(Class, pkid=pkid)

    if request.method == "POST":

        # extract information from the class form
        grade_level = request.POST.get("grade_level")
        class_name = request.POST.get("class_name")
        class_master = request.POST.get("class_master")
        class_prefect = request.POST.get("class_prefect")

        print(class_prefect, class_master)

        klass.grade_level = grade_level
        klass.class_name = class_name
        klass.class_master = class_master
        klass.class_prefect = class_prefect

        klass.save()
        save_and_add_flag = request.POST.get("save_and_add")
        if save_and_add_flag:
            print(save_and_add_flag)
            return redirect(reverse("class-add"))
        return redirect(reverse("class-list"))

    template_name = "classes/class-edit.html"
    context = {"section": "class-area", "class": klass}

    return render(request, template_name, context)


@login_required
def class_delete_view(request, pkid, *args, **kwargs):
    klass = get_object_or_404(Class, pkid=pkid)

    klass.delete()
    messages.success(request, "Class has been successfully deleted")

    return redirect(reverse("class-list"))


def verify_teacher_pin(request):
    if request.method == "POST":
        pin = request.POST.get("pin")
        email = request.POST.get("email")
        # Check if teacher exists with this email
        teachers = TeacherProfile.objects.filter(user__email=email)
        if teachers.exists():
            teacher = teachers.first()
        else:
            messages.error(request, "No teacher found with given email.")
            return redirect(reverse("users:user-login"))

        # Check if teacher temp profile exist with this information
        teacher_temp = get_teacher_temp_account(pin, email, teacher)

        if teacher_temp:
            # go ahead and send them the email to perform a reset
            send_password_reset_email(request, teacher.user, teacher_temp)
            return redirect(reverse("users:password_reset_done"))
        else:
            messages.error(request, "No pending setup for the given account")
            return redirect(reverse("users:user-login"))
    else:
        template_name = "accounts/verifypin-teacher.html"
        form = VerifyPinForm()
        context = {"form": form}

        return render(request, template_name, context)


@login_required
def teacher_dashboard(request):
    # check if current user is user of type teacher
    template_name = "teachers/teacher-dashboard.html"
    if request.user.is_teacher or request.user.is_staff:
        announcements = Announcement.objects.filter(visible_to_students=True)
        teacher = None
        if request.user.is_teacher:
            teacher = request.user.teacher_profile

        context = {
            "announcements": announcements,
            "teacher": teacher,
            # "total_pass_courses": pass_courses_count,
            # "total_cources_writen": marks.count(),
            # "total_courses": total_courses,
            # "payment_history": payment_history,
            # "events": events,
            # "class": student.current_class,
            # "class_enrolment": class_enrolment.count(),
        }
        return render(request, template_name, context)
    else:
        messages.error(request, "You are not allowed to be here.")
        return render(
            request, template_name, {"error_message": "You are not allowed to be here."}
        )


def student_dashboard(request):
    print(request.user.username)
    announcements = Announcement.objects.filter(visible_to_students=True)

    # grap the current user from the request
    user = request.user
    # check if the current user is of a student type
    if isinstance(user.student_profile, StudentProfile):
        student = user.student_profile
    else:
        messages.error(request, "Not a valid student instance")
        template_name = "base.html"
        context = {}
        return render(request, template_name, context)

    courses = student.get_all_subjects()
    total_courses = len(courses)

    # calculate fee percentage of fee payment
    percentage = 0

    passed_cources = []

    term = Term.objects.get(is_current=True)

    current_year = AcademicYear.objects.get(is_current=True)
    # Get the payment history for the current year
    fees = Fee.objects.filter(student=student, academic_year=current_year)
    payment_history = None

    if fees.exists:
        fee = fees.first()
        payment_history = student.payment_history.filter(fee=fee)
        percentage = None

    # get all the exam sessions ids so far for that term
    examination_session_ids = ExaminationSession.objects.filter(term=term).values_list(
        "pkid", flat=True
    )
    # Grab all the mark records associated to this student for that year.
    marks = student.student_marks.filter(exam_session__pkid__in=examination_session_ids)

    pass_courses_count = marks.filter(score__gte=10).count()

    # get all evernts that have to with the students
    events = Event.objects.filter(visible_to_students=True)

    class_enrolment = StudentProfile.objects.filter(current_class=student.current_class)

    template_name = "students/student-dashboard.html"
    context = {
        "announcements": announcements,
        "student": student,
        "total_pass_courses": pass_courses_count,
        "total_cources_writen": marks.count(),
        "total_courses": total_courses,
        "payment_history": payment_history,
        "events": events,
        "class": student.current_class,
        "class_enrolment": class_enrolment.count(),
    }
    return render(request, template_name, context)
