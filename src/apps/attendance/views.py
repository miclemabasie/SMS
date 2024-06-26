from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.students.models import StudentProfile, Subject, TeacherProfile, Class
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Attendance


@login_required
def take_attendance(request):
    user = request.user
    if not user.is_teacher:
        messages.error(request, "Not allowed")
        return redirect(reverse("users:user-login"))

    # get all subjects for this current teacher.
    teacher = user.teacher_profile

    assigned_subjects = Subject.objects.filter(assigned_to=teacher)
    filter_classes = []
    classes = []
    for sub in assigned_subjects:
        for cl in sub.classes.all():
            if cl.pkid not in filter_classes:
                filter_classes.append(cl.pkid)
                classes.append({"klass": cl, "subject": sub})

    subjects = Subject.objects.filter(assigned_to=teacher)
    template_name = "attendance/take-attendance.html"
    context = {
        "section": "attendance",
        "subjects": subjects,
        "classes": classes,
    }

    return render(request, template_name, context)


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    class_pkid = request.POST.get("class_id")
    subject = Subject.objects.get(pkid=subject_id)
    student_data = []
    students = StudentProfile.objects.filter(current_class__pkid=class_pkid)
    for student in students:
        data = {
            "id": student.pkid,
            "name": student.user.get_fullname,
        }
        student_data.append(data)
    return JsonResponse(
        json.dumps(student_data), content_type="application/json", safe=False
    )


@csrf_exempt
def save_attendance(request):
    user = request.user
    teacher = user.teacher_profile
    student_data = request.POST.get("student_ids")
    subject_id = request.POST.get("subject")
    class_id = request.POST.get("class_id")
    subject = Subject.objects.get(pkid=subject_id)

    students = json.loads(student_data)
    for student_dict in students:
        print(student_dict)
        # get the student
        student = get_object_or_404(StudentProfile, pkid=student_dict.get("id"))
        print("this is the the student", student)
        status = student_dict["status"]
        attendance = Attendance.objects.create(
            is_present=status, student=student, teacher=teacher, subject=subject
        )
        print("this is the att", attendance)
        # # check if attentance with same info already exist
        # date = attendance.created_at.date().day
        # att = Attendance.objects.filter(subject=subject, )
        attendance.save()

    # creat attendance records
    return HttpResponse("OK")


def view_attendance(request):

    user = request.user
    if not user.is_teacher:
        messages.error(request, "Not allowed")
        return redirect(reverse("users:user-login"))

    # get all subjects for this current teacher.
    teacher = user.teacher_profile

    assigned_subjects = Subject.objects.filter(assigned_to=teacher)
    filter_classes = []
    classes = []
    for sub in assigned_subjects:
        for cl in sub.classes.all():
            if cl.pkid not in filter_classes:
                filter_classes.append(cl.pkid)
                classes.append({"klass": cl, "subject": sub})

    subjects = Subject.objects.filter(assigned_to=teacher)

    template_name = "attendance/view-attendance.html"
    context = {
        "section": "attendance",
        "subjects": subjects,
        "classes": classes,
    }
    return render(request, template_name, context)


@csrf_exempt
def get_attendance(request):

    user = request.user
    if not user.is_teacher:
        messages.error(request, "Not allowed")
        return redirect(reverse("users:user-login"))

    # get all subjects for this current teacher.
    teacher = user.teacher_profile
    subject_id = request.POST.get("subject")
    class_id = request.POST.get("class_id")
    subject = Subject.objects.filter(pkid=subject_id).first()
    klass = Class.objects.filter(pkid=class_id).first()
    attendance_dates = []
    valid_attendances = []
    attendances = Attendance.objects.filter(subject=subject, teacher=teacher)
    for att in attendances:
        print(att.created_at)
        if att.created_at.date().day not in attendance_dates:
            attendance_dates.append(att.created_at.date().day)
            valid_attendances.append(att)
    try:
        attendance_list = []
        for attd in valid_attendances:
            data = {
                "id": attd.pkid,
                "attendance_date": str(attd.created_at),
                "session": klass.pkid,
            }
            attendance_list.append(data)
        return JsonResponse(json.dumps(attendance_list), safe=False)
    except Exception as e:
        print(e)
        return None


@csrf_exempt
def get_student_attendance(request):
    attendance_date_id = request.POST.get("attendance_date_id")
    # get the attendance for the given dateid
    attendance = Attendance.objects.get(pkid=attendance_date_id)
    subject_id = request.POST.get("subject")

    subject = Subject.objects.filter(pkid=subject_id).first()

    date = attendance.created_at.date().day
    # get all students
    student_data = []
    students_atts = Attendance.objects.filter(
        subject=subject, created_at__date__day=date
    )

    # create unique entries
    valid_ids = []
    students = []
    for att in students_atts:
        if not att.student.user.pkid in valid_ids:
            valid_ids.append(att.student.user.pkid)
            students.append(att)

    for attendance in students:
        data = {
            "id": attendance.student.user.pkid,
            "name": attendance.student.user.get_fullname,
            "status": attendance.is_present,
        }
        student_data.append(data)
    return JsonResponse(
        json.dumps(student_data), content_type="application/json", safe=False
    )


def update_attendance(request):
    HttpResponse("Ok")
