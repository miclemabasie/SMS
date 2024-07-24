from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.students.models import StudentProfile, Subject, TeacherProfile, Class
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Attendance, DailyAttendance
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()


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
        classes.append({"klass": sub.klass, "subject": sub})

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
        classes.append({"klass": sub.klass, "subject": sub})

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


def attendance_class_list_view(request):
    classes = Class.objects.all()

    template_name = "attendance/attendance-class-list.html"
    context = {
        "section": "attendance",
        "classes": classes,
    }

    return render(request, template_name, context)


def take_daily_attendance(request, class_pkid):
    """
    GET: send a list of all the students in the class.
    """
    classes = Class.objects.filter(pkid=class_pkid)
    if classes.exists():
        klass = classes.first()
    else:
        return redirect(reverse("attendance:attendance_class_list"))

    students = klass.students.all()
    print("this are the students", students)
    users = []
    for student in students:
        users.append(student.user)

    template_name = "attendance/take-daily-attendance.html"
    context = {
        "students": users,
        "klass": klass,
    }

    return render(request, template_name, context)


@csrf_exempt
def save_daily_attendance(request):
    admin_user = request.user
    if not admin_user.is_admin:
        messages.error(request, "Invalid Operation for this user account.")
        return redirect("users:user-login")
    else:
        admin_user = admin_user.admin_profile

    student_data = request.POST.get("student_ids")
    students = json.loads(student_data)

    for student_dict in students:
        user = get_object_or_404(User, pkid=student_dict.get("id"))
        status = student_dict["status"]

        # Get today's date without time component
        today = timezone.now().date()

        # Check if an attendance record for today already exists
        attendance, created = DailyAttendance.objects.update_or_create(
            user=user,
            day__date=today,
            defaults={"is_present": status, "taken_by": admin_user},
        )
        if created:
            print(f"Created new attendance for {user} on {today}")
        else:
            print(f"Updated attendance for {user} on {today}")

    return HttpResponse("OK")


def view_daily_attendance(request, class_pkid):
    date = request.GET.get("date")
    klass = get_object_or_404(Class, pkid=class_pkid)
    students = klass.students.all()

    # If no date is provided, default to today
    if date:
        date = timezone.datetime.strptime(date, "%Y-%m-%d").date()
    else:
        date = timezone.now().date()

    attendance_records = DailyAttendance.objects.filter(
        user__in=[student.user for student in students], day__date=date
    )

    # Create a dictionary to map student IDs to their attendance status
    attendance_dict = {att.user.pk: att.is_present for att in attendance_records}
    attendance_dict_pkids = {att.user.pk: att.pkid for att in attendance_records}

    context = {
        "klass": klass,
        "students": students,
        "attendance_dict": attendance_dict,
        "attendance_dict_pkids": attendance_dict_pkids,
        "date": date,
    }

    print(context)

    return render(request, "attendance/view-daily-attendance.html", context)


def edit_daily_attendance(request, class_pkid, attendance_pkid):
    if request.user.is_admin == False:
        messages.error(request, "Invalid request.")
        return redirect(
            reverse(
                "attendance:view_daily_attendance",
                kwargs={"class_pkid": class_pkid},
            )
        )

    if request.method == "POST":
        status = request.POST.get("status")
        try:
            status = int(status)
        except:
            messages.error(request, "Invalid request")
            return redirect(
                reverse(
                    "attendance:view_daily_attendance",
                    kwargs={"class_pkid": class_pkid},
                )
            )

        attendance = DailyAttendance.objects.get(pkid=attendance_pkid)
        attendance.is_present = status
        attendance.save()

        messages.success(request, "Attendance udpated.")
        return redirect(
            reverse(
                "attendance:view_daily_attendance",
                kwargs={"class_pkid": class_pkid},
            )
        )
