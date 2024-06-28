from django.shortcuts import render
from django.http import HttpResponse
from .models import AdminLeave, TeacherLeave, StudentLeave


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


def add_leave(request):
    pass

    return HttpResponse("ok")


def approve_leave(request):
    pass

    return HttpResponse("ok")


def reject_leave(request):
    pass
    return HttpResponse("ok")


def see_leave(request, pkid):
    pass
    return HttpResponse("ok")
