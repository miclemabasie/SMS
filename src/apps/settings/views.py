from django.shortcuts import render, redirect
from django.urls import reverse
from apps.terms.models import ExaminationSession, Term, AcademicYear
from .models import Setting
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse


from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse


def settings_view(request):
    if request.method == "POST":
        # Check if settings already exist in the database
        setting = Setting.objects.all().first()
        if setting:
            messages.error(request, "Settings already initialized.")
            return redirect(reverse("settings:settings-home"))

        setting = Setting.objects.create()
        setting.save()

        # Create the different groups needed to run the system
        students_group, _ = Group.objects.get_or_create(name="students")
        teachers_group, _ = Group.objects.get_or_create(name="teachers")
        admin_group, _ = Group.objects.get_or_create(name="administrator")

        # Define the permissions to add
        student_permissions = [
            "change_studentprofile",
            "change_class",
            "view_subject",
            "view_reportcard",
            "view_studentprofile",
            "view_announcement",
        ]

        teacher_permissions = [
            "add_mark",
            "change_mark",
            "view_mark",
            "add_attendance",
            "change_attendance",
            "view_attendance",
            "view_announcement",
        ]

        admin_permissions = [
            "add_announcement",
            "change_announcement",
            "delete_announcement",
            "view_announcement",
            # admin profile
            "add_adminprofile",
            "change_adminprofile",
            "view_adminprofile",
            "delete_adminprofile",
            # sessions
            "add_session",
            "change_session",
            "view_session",
            "delete_session",
            # subjects
            "add_subject",
            "change_subject",
            "view_subject",
            "delete_subject",
            # Attendance
            "add_attendance",
            "change_attendance",
            "delete_attendance",
            "view_attendance",
            # Managring clasess
            "add_class",
            "change_class",
            "delete_class",
            "view_class",
            # Marks management
            "add_mark",
            "change_mark",
            "delete_mark",
            "view_mark",
            # Managing students
            "add_studentprofile",
            "change_studentprofile",
            "delete_studentprofile",
            "view_studentprofile",
            # Managring teacher profiles
            "add_teacherprofile",
            "change_teacherprofile",
            "delete_teacherprofile",
            "view_teacherprofile",
            # Session management
            "add_academicyear",
            "change_academicyear",
            "delete_academicyear",
            "view_academicyear",
            "add_examinationsession",
            "change_examinationsession",
            "delete_examinationsession",
            "view_examinationsession",
            # Term Management
            "add_term",
            "change_term",
            "delete_term",
            "view_term",
            # Fee manaagement
            "add_fee",
            "change_fee",
            "delete_fee",
            "view_fee",
            "add_feepaymenthistory",
            "change_feepaymenthistory",
            "delete_feepaymenthistory",
            "view_feepaymenthistory",
            # Reportcards
            "add_reportcard",
            "change_reportcard",
            "delete_reportcard",
            "view_reportcard",
        ]

        # Initialize message container
        message = ""

        # Add student permissions to the group
        for perm in student_permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                students_group.permissions.add(permission)
                message += f'Permission "{perm}" added to group "students".\n'
            except Permission.DoesNotExist:
                message += f'Permission "{perm}" does not exist.\n'

        # Add teacher permissions to the group
        for perm in teacher_permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                teachers_group.permissions.add(permission)
                message += f'Permission "{perm}" added to group "teachers".\n'
            except Permission.DoesNotExist:
                message += f'Permission "{perm}" does not exist.\n'

        # Add admin permissions to the group
        for perm in admin_permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                admin_group.permissions.add(permission)
                message += f'Permission "{perm}" added to group "administrator".\n'
            except Permission.DoesNotExist:
                message += f'Permission "{perm}" does not exist.\n'

        # Flash success message
        messages.success(
            request, "Settings have been successfully initialized.\n" + message
        )
        return redirect(reverse("settings:settings-home"))

    setting = Setting.objects.all().first()

    template_name = "settings/settings.html"
    context = {"section": "settings", "setting": setting}

    return render(request, template_name, context)


def fee_settings(request):
    setting = Setting.objects.all().first()
    if request.method == "POST":
        # get the data from the form
        first_installment = request.POST.get("first_installment")
        second_installment = request.POST.get("second_installment")
        pta = request.POST.get("pta")
        school_uniform = request.POST.get("school_uniform")
        print(first_installment, second_installment)
        # update fee payment information
        setting.first_installment = first_installment
        setting.second_installment = second_installment
        setting.pta = pta
        setting.school_uniform = school_uniform
        setting.save()
        messages.success(request, "Fee payment updated successfully")
        return redirect(reverse("settings:settings-fees"))
    template_name = "settings/fee-settings.html"
    context = {"section": "settings", "setting": setting}

    return render(request, template_name, context)


def update_settings(request):
    settings = Setting.objects.all()
    if len(settings) > 0:
        setting = settings.first()
    else:
        messages.error(request, "Settings have not yet been initialized.")
        return redirect(reverse("settings:settings-home"))

    if request.method == "POST":
        # extract the fields
        data = request.POST
        school_name = data.get("school_name")
        currency = data.get("currency")
        country = data.get("country")
        city = data.get("city")
        address1 = data.get("address1")
        address2 = data.get("address2")
        postal = data.get("postal")
        motto = data.get("motto")
        logo = request.FILES.get("logo")
        favicon = request.FILES.get("favicon")

        print(logo)

        setting.school_name = school_name
        if currency:
            setting.currency = currency
        if country:
            setting.country = country
        if city:
            setting.city = city
        if address1:
            setting.address1 = address1
        if address2:
            setting.address2 = address2
        if postal:
            setting.postal_code = postal
        if motto:
            setting.motto = motto

        if logo:
            print("This is the logo", logo)
            setting.school_logo = logo
        if favicon:
            setting.school_favicon = favicon

        setting.save()

        messages.success(request, "Settings have been successfully updated")

        return redirect(reverse("settings:settings-home"))
    return redirect(reverse("settings:settings-home"))


def session_settings_view(request):

    sessions = AcademicYear.objects.all()
    current_session = sessions.filter(is_current=True).first()
    template_name = "settings/session-settings.html"
    context = {
        "section": "settings",
        "sessions": sessions,
        "current_session": current_session,
    }

    return render(request, template_name, context)


def term_settings_view(request):

    sessions = AcademicYear.objects.all()
    terms = Term.objects.all()

    current_session = sessions.filter(is_current=True).first()
    current_term = terms.filter(is_current=True).first()
    template_name = "settings/term-settings.html"
    context = {
        "section": "settings",
        "sessions": sessions,
        "terms": terms,
        "current_session": current_session,
        "current_term": current_term,
    }

    return render(request, template_name, context)


def exam_session_view(request):

    exam_sessions = ExaminationSession.objects.all()
    sessions = AcademicYear.objects.all()
    terms = Term.objects.all()

    current_session = sessions.filter(is_current=True).first()
    current_term = terms.filter(is_current=True).first()
    current_exam_session = ExaminationSession.objects.filter(is_current=True).first()

    template_name = "settings/exam-session.html"
    context = {
        "section": "settings",
        "sessions": sessions,
        "terms": terms,
        "exam_sessions": exam_sessions,
        "current_session": current_session,
        "current_term": current_term,
        "current_exam_session": current_exam_session,
    }

    return render(request, template_name, context)


# To be done later
def add_class_pass_avg(request):
    pass


def toggle_teacher_can_upload_marks_permission(request):
    if request.method == "POST":
        permission_to_upload_status = request.POST.get("status")
        setting = Setting.objects.all().first()
        print(setting.teacher_can_upload)
        setting.teacher_can_upload = permission_to_upload_status
        setting.save()
        print(setting.teacher_can_upload)
        return JsonResponse({"status": 1}, safe=False)
    template_name = "settings/permissions.html"
    context = {
        "section": "settings",
    }

    return render(request, template_name, context)
