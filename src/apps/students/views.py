from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import VerifyPinForm
from .utils import (
    check_student_is_owing,
    check_student_is_repeater,
    create_student_pin,
    get_student_temp_account,
    get_teacher_temp_account,
    send_account_creation_email,
    send_password_reset_email,
    format_date,
    generate_random_pin,
)
from .models import (
    StudentProfile,
    Class,
    Subject,
    Mark,
    TeacherProfile,
    StudentTempCreateProfile,
    TeacherTempCreateProfile,
)

from apps.terms.models import ExaminationSession, AcademicYear, Term
from django.contrib.auth import get_user_model
from apps.profiles.models import ParentProfile
from apps.fees.models import Fee
from datetime import datetime, timezone, time
from django.contrib.auth.decorators import login_required
import random
import openpyxl
from django.http import HttpResponse
from openpyxl.utils import get_column_letter
import csv
from django.contrib import messages
from openpyxl import workbook, load_workbook
import json
from django.http import JsonResponse

from apps.attendance.models import Attendance

User = get_user_model()

from faker import Faker

faker = Faker()


@login_required
def list_student_view(request):

    queryset = StudentProfile.objects.all()
    template_name = "students/list.html"
    context = {
        "section": "student-area",
        "students": queryset,
    }

    return render(request, template_name, context)


@login_required
def student_detail_view(request, matricule, pkid):
    fee = None
    payment_history = None
    student = get_object_or_404(StudentProfile, matricule=matricule, pkid=pkid)
    # get the current academic year
    current_year = AcademicYear.objects.get(is_current=True)

    # Get the payment history for the current year
    fees = Fee.objects.filter(student=student, academic_year=current_year)

    if fees.exists:
        fee = fees.first()
        payment_history = student.payment_history.filter(fee=fee)

    # Grab all the mark records associated to this student
    marks = student.student_marks.all()

    # Get all the subjects in the class the student belongs to
    # and those optionally added by the student
    subjects1 = student.current_class.subjects.all()
    # get optoinal subjects for the particular student
    optional_subjects = student.optional_subjects.all()

    distinct_subjects = set(list(subjects1) + list(optional_subjects))

    pin = StudentTempCreateProfile.objects.filter(student=student)
    if pin.exists():
        pin = pin.first()
    else:
        pin = None

    template_name = "students/details.html"
    context = {
        "section": "student-area",
        "student_detial_section": True,
        "student": student,
        "payment_history": payment_history,
        "number_of_payments": len(payment_history),
        "marks": marks,
        "subjects": distinct_subjects,
        "fee": fee,
        "pin": pin,
    }

    return render(request, template_name, context)


@login_required
def add_student_view(request):
    classes = Class.objects.all()
    if request.method == "POST":
        print(request.POST)

        pin = request.POST.get("password_reset_pin")
        parent_fname = request.POST.get("first_name")
        parent_occupation = request.POST.get("parent-occupation")
        parent_phone = request.POST.get("parent-phone")
        parent_email = request.POST.get("parent-email")
        parent_address = request.POST.get("parent-address")
        parent_role = request.POST.get("parent-role")

        st_class = request.POST.get("student_class")

        # Check if student pin is valid
        # should not be greater or less than 4 in length
        if len(pin) == 4:
            # create temp
            pass
        else:
            messages.error(
                "Password reset pin has incorrect length, should be exactly 4."
            )
            return redirect(reverse("students:student-add"))

        # Get class in which student is part of
        student_class = get_object_or_404(Class, pkid=int(st_class))

        # Create parent for student
        student_parent, created = ParentProfile.objects.get_or_create(
            first_name=parent_fname,
            phone=parent_phone,
            occupation=parent_occupation,
            address=parent_address,
            email=parent_email,
            role=parent_role,
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

        dob = datetime.strptime(date_string_from_form, "%Y-%m-%d").date()
        # Create a specific time
        specific_time = time(8, 51, 2)

        dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)

        # Construct faker usernames, this is done assuming that the usernames are not important to the students
        # we avoid using direct fake usernames, so as to avoid unique constrainst failure in the database
        # This is why the random digit is added to the end of every fake username generated by faker
        # faker_username = st_fname
        # attache random digit to the end
        # faker_username + str(random.randint(0, 9))

        if not st_email:
            st_email = faker.email()

        user, created = User.objects.get_or_create(
            username=st_fname,
            first_name=st_fname,
            last_name=st_lname,
            email=st_email,
            is_student=True,
            dob=dob_with_time,
        )
        if created:
            user.save()

        # Create student instance

        student, created = StudentProfile.objects.get_or_create(
            user=user,
            parent=student_parent,
            current_class=student_class,
            gender=st_gender,
            phone_number=st_phone,
            # profile_photo=st_photo,
            address=st_address,
            domain=st_domain,
        )

        if created:

            student.save()
            if st_image:
                student.profile_photo = st_image
            student.save()
            create_student_pin(student, pin)
            send_account_creation_email(request, student.user)
            return redirect(reverse("students:student-list"))
        else:
            messages.error(request, "Student already exist.")
            return redirect(reverse("students:student-list"))

    template_name = "students/add.html"

    context = {"section": "student-area", "classes": classes}

    return render(request, template_name, context)


@login_required
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

        # Parse date string from form
        dob = datetime.strptime(st_dob, "%Y-%m-%d").date()
        specific_time = time(8, 51, 2)

        dob_with_time = datetime.combine(dob, specific_time, tzinfo=timezone.utc)
        # <class 'datetime.datetime'>
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
        return redirect(
            reverse(
                "students:student-detail",
                kwargs={"pkid": student.pkid, "matricule": student.matricule},
            )
        )

    # Get and associate a parent to the request.
    parent = student.parent
    template_name = "students/edit.html"
    context = {
        "section": "student_area",
        "student_profile": student,
        "dob": str(student.user.dob.date()),
        "classes": Class.objects.all(),
    }

    return render(request, template_name, context)


@login_required
def download_marksheet(request, subject_pkid, class_pkid, *args, **kwargs):
    # Get the class for which the mark sheet needs to be downloaded}|

    klass = get_object_or_404(Class, pkid=class_pkid)

    current_academic_session = AcademicYear.objects.filter(is_current=True).first()
    current_exam_session = ExaminationSession.objects.filter(is_current=True).first()
    if request.method == "POST":

        subject = get_object_or_404(Subject, pkid=subject_pkid)
        # Fetch all the students associated with the class
        students = klass.students.all()
        # Create a new workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "marks"

        # Define column headers
        headers = [
            "Matricule",
            "Full Name",
            "Mark",
        ]

        # Write headers to the first row
        for col_num, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header

        # Write student data to the worksheet
        for row_num, student in enumerate(students, start=2):
            ws.cell(row=row_num, column=1).value = student.matricule
            ws.cell(row=row_num, column=2).value = student.user.get_fullname

        # Set column widths
        for col_num in range(1, len(headers) + 1):
            column_letter = get_column_letter(col_num)
            ws.column_dimensions[column_letter].width = 20

        # Create a response object
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        filename = f"{klass.grade_level}-{klass.class_name}-{subject.name}.xlsx"
        response["Content-Disposition"] = f"attachment; filename={filename}"

        # Save the workbook to the response
        wb.save(response)

        return response

    template_name = "students/marks-sheet-download.html"
    context = {"section": "marks-area"}
    return render(request, template_name, context)


@login_required
def upload_marks1(request, subject_pkid, class_pkid, *args, **kwargs):
    # Get the subject and all the students associated to thesubject from the database

    subject = Subject.objects.get(pkid=subject_pkid)
    klass = Class.objects.get(pkid=class_pkid)
    academic_year = AcademicYear.objects.filter(is_current=True).first()

    terms = Term.objects.filter(academic_year=academic_year)

    sequences = []

    for term in terms:
        for ex_session in term.examination_sessions.all():
            sequences.append(ex_session)

    if request.method == "POST" and request.FILES["marks_file"]:
        marks_file = request.FILES["marks_file"]

        selected_ex_session_id = request.POST.get("selected_ex_session")
        exam_session = ExaminationSession.objects.filter(pkid=selected_ex_session_id)
        if exam_session.exists():
            exam_session = exam_session.first()
        else:
            messages.error(request, "Invalid Exam Session")
            return redirect(
                reverse(
                    "students:marks-upload",
                    kwargs={"subject_pkid": subject_pkid, "class_pkid": class_pkid},
                )
            )

        # decoded_file = marks_file.read().decode('utf-8').splitlines()

        # Get the teacher from the DB
        teacher = request.user.teacher_profile

        # Get the subject from the database

        wb = load_workbook(filename=marks_file)

        ws = wb["marks"]

        for row in ws.iter_rows(min_row=2, values_only=True):
            student_matricule, subject_name, marks = (
                row[0],
                row[1],
                row[2],
            )
            print(
                f"this is the student information student mat: {student_matricule}, mark: {marks}, subjectname: {subject_name}, subject_id: {subject.name}"
            )
            student = StudentProfile.objects.get(matricule=student_matricule)
            # Check if a mark already exists for this student and subject
            mark, created = Mark.objects.get_or_create(
                student=student, subject=subject, exam_session=exam_session
            )

            mark.teacher = teacher

            # Update the score
            if not marks:
                marks = 0
            mark.score = marks
            mark.save()
            print(mark)

        messages.success(
            request,
            f"Marks have been updated for the subject: `{subject.name}` by: `{teacher.user.username}` with matricule No: {teacher.matricule}",
        )
        return redirect(reverse("students:marks"))

    template_name = "students/upload-marks.html"
    context = {
        "section": "marks-area",
        "subject": subject,
        "klass": klass,
        "sessions": sequences,
        "year": academic_year,
    }

    return render(request, template_name, context)


# @login_required
# def upload_marks(request, class_pkid, *args, **kwargs):
#     # Get the subject and all the students associated to thesubject from the database

#     klass = get_object_or_404(Class, pkid=class_pkid)
#     if request.method == "POST" and request.FILES["marks_file"]:
#         marks_file = request.FILES["marks_file"]
#         teacher_matricule = request.POST.get("teacher_matricule")
#         selected_subject_id = request.POST.get("selected_subject_id")

#         print(
#             "This is the information from the form: ",
#             teacher_matricule,
#             selected_subject_id,
#         )

#         # decoded_file = marks_file.read().decode('utf-8').splitlines()

#         # Get the teacher from the DB
#         teachers = TeacherProfile.objects.filter(matricule=teacher_matricule)
#         if teachers.exists():
#             teacher = teachers.first()
#         else:
#             messages.error(request, "No Teacher found with the given matricule")
#             return redirect(
#                 reverse("students:marks-upload", kwargs={"class_pkid": class_pkid})
#             )

#         # Get the subject from the database
#         subjects = Subject.objects.filter(pkid=selected_subject_id)
#         if subjects.exists():
#             subject = subjects.first()
#         else:
#             messages.error(request, "Subject not found.")
#             return redirect(
#                 reverse("students:marks-uploads", kwargs={"class_pkid": class_pkid})
#             )

#         # Get the session
#         exam_session = ExaminationSession.objects.get(is_current=True)

#         wb = load_workbook(filename=marks_file)

#         ws = wb["marks"]

#         for row in ws.iter_rows(min_row=2, values_only=True):
#             student_matricule, marks, subject_name, subject_id = (
#                 row[0],
#                 row[3],
#                 row[6],
#                 row[7],
#             )
#             print(
#                 f"this is the student information student mat: {student_matricule}, mark: {marks}, subjectname: {subject_name}, subject_id: {subject_id}"
#             )
#             student = StudentProfile.objects.get(matricule=student_matricule)
#             # Check if a mark already exists for this student and subject
#             mark, created = Mark.objects.get_or_create(
#                 student=student, subject=subject, exam_session=exam_session
#             )

#             mark.teacher = teacher

#             # Update the score
#             if not marks:
#                 marks = 0
#             mark.score = marks
#             mark.save()
#             print(mark)

#         messages.success(
#             request,
#             f"Marks have been updated for the subject: `{subject.name}` by: `{teacher.user.username}` with matricule No: {teacher.matricule}",
#         )
#         return redirect(reverse("students:marks"))

#     template_name = "students/upload-marks.html"
#     context = {
#         "section": "marks-area",
#         "class": klass,
#         "subjects": Subject.objects.all(),
#     }

#     return render(request, template_name, context)


@login_required
def marks(request):
    user = request.user
    if user.is_teacher or user.is_admin:
        if user.is_teacher:
            # get all assigned subject to the current teacher.
            teacher = user.teacher_profile
            assigned_subjects = Subject.objects.filter(assigned_to=teacher)
            filter_classes = []
            classes = []
            for sub in assigned_subjects:
                if sub.klass == None:
                    continue
                classes.append({"klass": sub.klass, "subject": sub})

            print(classes)
        
        if len(classes) < 1:
            classes = None

        print("########### this is the class", classes)

        template_name = "students/marks.html"
        context = {
            "section": "marks-area",
            "classes": classes,
            "subjects": Subject.objects.all(),
        }

        return render(request, template_name, context)
    else:
        messages.error(request, "Unauthorized..")
        return redirect(reverse("users:user-login"))


def list_student_record(request, pkid, matricule, *args, **kwargs):

    # Grab all the mark records associated to this student
    student = get_object_or_404(StudentProfile, pkid=pkid, matricule=matricule)

    marks = student.student_marks.all()

    template_name = "students/academic-records.html"

    context = {"section": "student-area", "marks": marks, "student": student}

    return render(request, template_name, context)


def add_optional_subjects_to_student(
    request, student_pkid, student_matricule, *args, **kwargs
):

    student = get_object_or_404(
        StudentProfile, pkid=student_pkid, matricule=student_matricule
    )
    # Get all the subjects in the class the student belongs to
    # and those optionally added by the student
    subjects1 = student.current_class.subjects.all()
    # get optoinal subjects for the particular student
    optional_subjects = student.optional_subjects.all()

    distinct_subjects = set(list(subjects1) + list(optional_subjects))

    subjects = Subject.objects.all()

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
            "we are inside the loop", len(optional_subjects), len(selected_subjects_ids)
        )
        if len(optional_subjects) > 0 and len(selected_subjects_ids) > 0:
            for subject in optional_subjects:
                print("This is the subject", subject)
                student.optional_subjects.remove(subject)
                student.save()

        print(student.optional_subjects.all())

        # Reassign the subjects to the klass instance
        # Ge throught the incoming ids, and get the subjects associated the with the pkids
        for pkid in selected_subjects_ids:
            sub = Subject.objects.filter(pkid=pkid).first()
            if sub:
                student.optional_subjects.add(sub)
                student.save()

        return JsonResponse({"message": "updated."})

    template_name = "students/add-optional-subjects.html"
    context = {
        "selected_subjects": distinct_subjects,
        "unselected_subjects": subjects,
        "student": student,
    }

    return render(request, template_name, context)


@login_required
def download_class_list(request, *args, **kwargs):
    # Get the class
    if request.method == "POST":
        class_pkid = int(request.POST.get("selected_class_id"))

        # Check if there is a class given class_id
        classes = Class.objects.filter(pkid=class_pkid)
        if classes.exists():
            klass = classes.first()
        else:
            return redirect(reverse("students:student-list"))

        students = StudentProfile.objects.filter(current_class=klass)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"{klass.grade_level}-{klass.class_name}"

        headers = [
            "Matricule",
            "Fullname",
            "DOB",
            "Parent",
            "Gender",
            "IS Owing",
            "Is Repeater",
        ]

        # Write headers to the first row
        for col_num, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header

        # Write student data to the worksheet
        for row_num, student in enumerate(students, start=2):
            ws.cell(row=row_num, column=1).value = student.matricule
            ws.cell(row=row_num, column=2).value = student.user.get_fullname
            ws.cell(row=row_num, column=3).value = student.user.dob.year
            ws.cell(row=row_num, column=4).value = student.parent.first_name
            # ws.cell(row=row_num, column=4).value = current_academic_session.name
            ws.cell(row=row_num, column=5).value = student.gender
            ws.cell(row=row_num, column=6).value = check_student_is_owing(student.pkid)
            ws.cell(row=row_num, column=7).value = check_student_is_repeater(
                student_pkid=student.pkid
            )

        # Set column widths
        for col_num in range(1, len(headers) + 1):
            column_letter = get_column_letter(col_num)
            ws.column_dimensions[column_letter].width = 20

        # Create a response object
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f"attachment; filename={klass.grade_level}-{klass.class_name}-class-list.xlsx"
        )

        # Save the workbook to the response
        wb.save(response)

        return response
    return redirect(reverse("students:student-list"))


@login_required
def upload_students_from_file(request, *args, **kwargs):
    # Get the subject and all the students associated to thesubject from the database

    classes = Class.objects.all()
    if request.method == "POST" and request.FILES["students_file"]:
        students_file = request.FILES["students_file"]
        selected_class_id = request.POST.get("selected_class_id")

        print("incoming data", students_file, selected_class_id)

        # decoded_file = students_file.read().decode('utf-8').splitlines()

        # Get the subject from the database
        classes = Class.objects.filter(pkid=selected_class_id)
        if classes.exists():
            klass = classes.first()
        else:
            messages.error(request, "Class not found.")
            return redirect(reverse("students:upload-students-from-file"))

        wb = load_workbook(filename=students_file)

        ws = wb.get_sheet_by_name("Student Upload Sample File")

        # Check if all the attributes need to create the user and student profile are available inthe file
        for row in ws.iter_rows(min_row=2, values_only=True):
            first_name, last_name, email, dob, gender, phone, address = (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
            )
            attributes = [first_name, last_name, gender, phone]
            for value in attributes:
                if not value:
                    messages.error(request, "Invalid file, missing information")
                    return redirect(reverse("students:upload-students-from-file"))

        for row in ws.iter_rows(min_row=2, values_only=True):
            first_name, last_name, email, dob, gender, phone, address = (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
            )

            print(
                f"fistname {first_name}, lastname {last_name}, email {email}, dob {dob} gender {gender} phone {phone} address {address}"
            )

            # Create user

            dob = format_date(dob)
            print(dob)
            if not email:
                intial_string = first_name
                email = f"{intial_string}{random.randint(1, 10)}@gmail.com"
                print(email)
            user, created = User.objects.get_or_create(
                username=f"{first_name}",
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            if dob:
                dob = datetime.combine(dob, dob.time(), tzinfo=timezone.utc)
                user.dob = dob

            if created:
                user.save()
                print(user)
                print("user was saved")

            # create student profile instance
            if gender.lower() == "m" or gender.lower() == "male":
                gender = "Male"
            else:
                gender = "Female"
            student, created = StudentProfile.objects.get_or_create(
                user=user,
                current_class=klass,
                gender=gender,
                phone_number=str(phone),
            )

            if created:

                if not address:
                    student.address = faker.address()

                print("Saving student")
                student.save()
                student.user.is_student = True
                create_student_pin(student, generate_random_pin())
                send_account_creation_email(request, student.user)
            else:
                continue
        messages.success(
            request,
            f"Students have been uploaded for the class {klass.grade_level}-{klass.class_name}",
        )
        return redirect(reverse("students:upload-students-from-file"))

    template_name = "students/upload-students.html"
    context = {
        "section": "marks-area",
        "classes": classes,
    }

    return render(request, template_name, context)


@login_required
def download_sample_student_file(request, *args, **kwargs):

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Student Upload Sample File"

    headers = [
        "First Name",
        "Last Name",
        "Email",
        "Date Of Birth",
        "Gender",
        "Phone Number",
        "Address",
    ]

    # Write headers to the first row
    for col_num, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header

    # Set column widths
    for col_num in range(1, len(headers) + 1):
        column_letter = get_column_letter(col_num)
        ws.column_dimensions[column_letter].width = 20

    # Create a response object
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f"attachment; filename=student_upload_sample_file.xlsx"
    )

    # Save the workbook to the response
    wb.save(response)

    return response


def verify_student_pin(request):
    if request.method == "POST":
        pin = request.POST.get("pin")
        email = request.POST.get("email")
        # Check if student exists with this email
        students = StudentProfile.objects.filter(user__email=email)
        if students.exists():
            student = students.first()
        else:
            messages.error(request, "No student found with given email.")
            return redirect(reverse("users:user-login"))

        # Check if student temp profile exist with this information
        student_temp = get_student_temp_account(pin, email, student)

        if student_temp:
            # go ahead and send them the email to perform a reset
            send_password_reset_email(request, student.user, student_temp)
            return redirect(reverse("users:password_reset_done"))
        else:
            messages.error(request, "No pending setup for the given account")
            return redirect(reverse("users:user-login"))
    else:
        template_name = "accounts/verifypin.html"
        form = VerifyPinForm()
        context = {"form": form}

        return render(request, template_name, context)


from apps.announcements.models import Announcement, Event, Category


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
    fee_percentage_paid = 100  # to be revisited.

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

    # get present absent data
    student_attendance_present = Attendance.objects.filter(
        student=student, is_present=True
    )
    student_attendance_absent = Attendance.objects.filter(
        student=student, is_present=False
    )

    data_absent_list = []
    data_present_list = []
    data_name_list = []
    for sub in courses:
        data_name_list.append(sub.name)
        # get the sum of all attendances for this subject
        total_attendance_per_sub_present = student_attendance_present.filter(
            subject=sub, is_present=True
        ).count()
        total_attendance_per_sub_absent = student_attendance_absent.filter(
            subject=sub, is_present=False
        ).count()
        data_present_list.append(total_attendance_per_sub_present)
        data_absent_list.append(total_attendance_per_sub_absent)

    total_present = student_attendance_present.count()
    total_absent = student_attendance_absent.count()
    total = total_present + total_absent
    percent_present = round(((total_present / total) * 100), 2)
    percent_absent = round(((total_absent / total) * 100), 2)
    template_name = "dashboards/student/student-dashboard.html"

    context = {
        "section": "student-dashboard",
        "announcements": announcements,
        "student": student,
        "total_pass_courses": pass_courses_count,
        "total_cources_writen": marks.count(),
        "total_courses": total_courses,
        "payment_history": payment_history,
        "events": events,
        "class": student.current_class,
        "class_enrolment": class_enrolment.count(),
        "fee_percentage_paid": fee_percentage_paid,
        "max_fee_percent": 0,
        # chat information
        "percent_present": percent_present,
        "percent_absent": percent_absent,
        "data_name": data_name_list,
        "data_absent": data_absent_list,
        "data_present": data_present_list,
    }

    print(context)
    return render(request, template_name, context)
