from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile, Subject, Class
from apps.profiles.models import ParentProfile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.contrib.auth import get_user_model
from apps.attendance.models import Attendance

User = get_user_model()


@login_required
def admin_dashboard(request):

    students = StudentProfile.objects.all().count()
    teachers = TeacherProfile.objects.all().count()
    parents = ParentProfile.objects.all().count()
    classes = Class.objects.all().count()

    # construct data for the header
    header = {
        "students": students,
        "teachers": teachers,
        "parents": parents,
        "classes": classes,
    }

    # Generate data about school attendance
    attendance_list_tuples = []
    class_list = []
    student_total_list_perclass = []
    for klass in Class.objects.all():
        class_list.append(klass.get_class_name)
        # got through all the students for a given klass
        students = StudentProfile.objects.filter(current_class=klass)
        total_present = 0
        total_absent = 0
        total_students = 0
        for std in students:
            total_students += 1
            print(std)
            # get all the attendance record of every student
            std_attendance_present = Attendance.objects.filter(
                student=std, is_present=True
            )
            std_attendance_absent = Attendance.objects.filter(
                student=std, is_present=False
            )
            print(std_attendance_present)
            print(std_attendance_absent)
            total_present += std_attendance_present.count()
            total_absent += std_attendance_absent.count()
        attendance_list_tuples.append((total_present, total_absent))
        student_total_list_perclass.append(total_students)

    """
    this is example output of the above operation
    ['Form 4-Science', 'Form 5-Kyle Miles', 'Form 6-S2', 'Form 7-S1', 'form1-Form 1 a', 'Form 4-Arts'] [(0, 0), (0, 0), (7, 1), (0, 0), (0, 0), (0, 0)]
    """
    print(student_total_list_perclass)
    # Calculate percentage of attendance
    attendance_list = []
    for att in attendance_list_tuples:
        # sub absent and present to get the total
        total_present = att[0]
        total_absent = att[1]
        total = total_present + total_absent
        if total > 0:
            # calculate percentage of attendance
            att_percentage = (total_present / total) * 100
            attendance_list.append(att_percentage)
        else:
            attendance_list.append(0)

    template_name = "dashboards/staff/dashboard.html"
    context = {
        "section": "admin-area",
        "header": header,
        "subject_list": class_list,
        "class_name_list": class_list,
        "attendance_list": attendance_list,
        "student_count_per_class": student_total_list_perclass,
    }

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
