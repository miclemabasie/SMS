from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.students.utils import format_date

from .models import AdminLeave, StudentLeave, TeacherLeave


@login_required
def list_leave(request):
    teacher_leaves = TeacherLeave.objects.filter(status="Pending")
    admin_leaves = AdminLeave.objects.filter(status="Pending")
    student_leaves = StudentLeave.objects.filter(status="Pending")

    template_name = "leave/list.html"
    context = {
        "teachers": teacher_leaves,
        "admins": admin_leaves,
        "students": student_leaves,
    }

    return render(request, template_name, context)


@login_required
def get_user_leaves(request):
    # check the type of user
    user_type = request.session.get("user_type")
    template_name = "leave/list-person.html"
    context = {
        "user_type": user_type,
        "section": "leave-per-person",
    }

    if user_type == "teacher":
        teacher = request.user.teacher_profile
        leaves = TeacherLeave.objects.filter(teacher=teacher)
        context.update({"leaves": leaves})

        return render(request, template_name, context)
    if user_type == "student":
        student = request.user.student_profile
        leaves = StudentLeave.objects.filter(student=student)
        context.update({"leaves": leaves})
        return render(request, template_name, context)
    if user_type == "admin":
        admin = request.user.admin_profile
        leaves = AdminLeave.objects.filter(admin=admin)
        context.update({"leaves": leaves})
        return render(request, template_name, context)


def add_leave(request):
    # check the type of user
    user_type = request.session.get("user_type")
    template_name = "leave/add.html"
    context = {
        "user_type": user_type,
        "section": "leave-per-person",
    }
    if request.method == "POST":
        # get the information from the form
        leave_date = request.POST.get("leave_date")
        duration = request.POST.get("duration")
        reason = request.POST.get("reason")

        date = format_date(leave_date)

        if user_type == "teacher":
            teacher = request.user.teacher_profile
            leave = TeacherLeave.objects.create(
                teacher=teacher,
                duration=duration,
                leave_date=date,
                reason=reason,
            )
            leave.save()
            messages.success(request, "Leave application successfull")
            return redirect(reverse("leave:leave-per-person"))
        if user_type == "student":
            student = request.user.student_profile
            leave = StudentLeave.objects.create(
                student=student,
                duration=duration,
                leave_date=date,
                reason=reason,
            )
            leave.save()
            messages.success(request, "Done")
            return redirect(reverse("leave:leave-per-person"))
        if user_type == "admin":
            admin = request.user.admin_profile
            leave = AdminLeave.objects.create(
                admin=admin,
                duration=duration,
                leave_date=date,
                reason=reason,
            )
            leave.save()
            messages.success(request, "Done")
            return redirect(reverse("leave:leave-per-person"))

    return render(request, template_name, context)


def approve_leave(request, leave_pkid, leave_type):
    # get the leave with the given id
    if leave_type == "teacher":
        leave = TeacherLeave.objects.get(pkid=leave_pkid)
    elif leave_type == "admin":
        leave = AdminLeave.objects.get(pkid=leave_pkid)
    elif leave_type == "student":
        leave = StudentLeave.objects.get(pkid=leave)

    leave.approval_status = "Approved"
    leave.save()
    messages.success(request, "Leave approved")
    return redirect(reverse("leave:list-leave"))


def reject_leave(request, leave_pkid, leave_type):
    # get the leave with the given id
    if leave_type == "teacher":
        leave = TeacherLeave.objects.get(pkid=leave_pkid)
    elif leave_type == "admin":
        leave = AdminLeave.objects.get(pkid=leave_pkid)
    elif leave_type == "student":
        leave = StudentLeave.objects.get(pkid=leave)

    leave.approval_status = "Rejected"
    leave.save()
    messages.success(request, "Leave Rejected")
    return redirect(reverse("leave:list-leave"))


def see_leave(request, pkid):
    pass
    return HttpResponse("ok")
