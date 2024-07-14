from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
    Subject,
    TeacherTempCreateProfile,
)
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from apps.leave.models import TeacherLeave
import json
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
        # extras
        region_of_origin = request.POST.get("region_of_origin")
        division_of_origin = request.POST.get("division_of_origin")
        sub_division_of_origin = request.POST.get("sub_division_of_origin")
        date_recruitement_public_service = request.POST.get(
            "date_recruitement_public_service"
        )
        corps = request.POST.get("corps")
        career_grade = request.POST.get("career_grade")
        payroll_grade = request.POST.get("payroll_grade")
        career_category = request.POST.get("career_category")
        payroll_category_solde = request.POST.get("payroll_category_solde")
        career_index = request.POST.get("career_index")
        payroll_index = request.POST.get("payroll_index")
        career_echelon = request.POST.get("career_echelon")
        payroll_echelon = request.POST.get("payroll_echelon")
        service = request.POST.get("service")
        appointed_structure = request.POST.get("appointed_structure")
        town = request.POST.get("town")
        possition_rank = request.POST.get("possition_rank")
        longivity_of_post = request.POST.get("longivity_of_post")
        longivity_in_administration = request.POST.get("longivity_in_administration")
        appointment_decision_reference = request.POST.get(
            "appointment_decision_reference"
        )
        indemnity_situation = request.POST.get("indemnity_situation")

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
        teacher.region_of_origin = region_of_origin
        teacher.division_of_origin = division_of_origin
        teacher.sub_division_of_origin = sub_division_of_origin
        teacher.date_recruitement_public_service = date_recruitement_public_service
        teacher.corps = corps
        teacher.career_grade = career_grade
        teacher.payroll_grade = payroll_grade
        teacher.career_category = career_category
        teacher.payroll_category_solde = payroll_category_solde
        teacher.career_index = career_index
        teacher.payroll_index = payroll_index
        teacher.career_echelon = career_echelon
        teacher.payroll_echelon = payroll_echelon
        teacher.service = service
        teacher.appointed_structure = appointed_structure
        teacher.town = town
        teacher.possition_rank = possition_rank
        teacher.longivity_of_post = longivity_of_post
        teacher.longivity_in_administration = longivity_in_administration
        teacher.appointment_decision_reference = appointment_decision_reference
        teacher.indemnity_situation = indemnity_situation

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

        # extras
        region_of_origin = request.POST.get("region_of_origin")
        division_of_origin = request.POST.get("division_of_origin")
        sub_division_of_origin = request.POST.get("sub_division_of_origin")
        date_recruitement_public_service = request.POST.get(
            "date_recruitement_public_service"
        )
        corps = request.POST.get("corps")
        career_grade = request.POST.get("career_grade")
        payroll_grade = request.POST.get("payroll_grade")
        career_category = request.POST.get("career_category")
        payroll_category_solde = request.POST.get("payroll_category_solde")
        career_index = request.POST.get("career_index")
        payroll_index = request.POST.get("payroll_index")
        career_echelon = request.POST.get("career_echelon")
        payroll_echelon = request.POST.get("payroll_echelon")
        service = request.POST.get("service")
        appointed_structure = request.POST.get("appointed_structure")
        town = request.POST.get("town")
        possition_rank = request.POST.get("possition_rank")
        longivity_of_post = request.POST.get("longivity_of_post")
        longivity_in_administration = request.POST.get("longivity_in_administration")
        appointment_decision_reference = request.POST.get(
            "appointment_decision_reference"
        )
        indemnity_situation = request.POST.get("indemnity_situation")

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
            teacher.region_of_origin = region_of_origin
            teacher.division_of_origin = division_of_origin
            teacher.sub_division_of_origin = sub_division_of_origin
            teacher.date_recruitement_public_service = date_recruitement_public_service
            teacher.corps = corps
            teacher.career_grade = career_grade
            teacher.payroll_grade = payroll_grade
            teacher.career_category = career_category
            teacher.payroll_category_solde = payroll_category_solde
            teacher.career_index = career_index
            teacher.payroll_index = payroll_index
            teacher.career_echelon = career_echelon
            teacher.payroll_echelon = payroll_echelon
            teacher.service = service
            teacher.appointed_structure = appointed_structure
            teacher.town = town
            teacher.possition_rank = possition_rank
            teacher.longivity_of_post = longivity_of_post
            teacher.longivity_in_administration = longivity_in_administration
            teacher.appointment_decision_reference = appointment_decision_reference
            teacher.indemnity_situation = indemnity_situation

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
            messages.warning(request, "Teacher already exists.")
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
        promotion_avg = request.POST.get("promotion_average")

        print(class_prefect, class_master)

        klass.grade_level = grade_level
        klass.class_name = class_name
        klass.class_master = class_master
        klass.class_prefect = class_prefect
        klass.pass_avg = promotion_avg

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
    template_name = "dashboards/teachers/teacher-dashboard.html"
    if request.user.is_teacher or request.user.is_staff:
        announcements = Announcement.objects.filter(visible_to_students=True)
        teacher = None
        if request.user.is_teacher:
            teacher = request.user.teacher_profile

            assigned_subjects = Subject.objects.filter(assigned_to=teacher)

        # get the number of classes teacher is involved with
        klasses = []
        for sub in assigned_subjects:
            if sub.klass not in klasses:
                klasses.append(sub.klass)

        # Get all the leave for this teacher
        leaves = TeacherLeave.objects.filter(teacher=teacher).count()
        total_leave = 0
        if leaves > 0:
            total_leave = leaves

        # get all the events made for teachers
        events = Event.objects.filter(visible_to_teachers=True)

        context = {
            "announcements": announcements,
            "teacher": teacher,
            "assigned_subjects": assigned_subjects,
            "assigned_subjects_count": assigned_subjects.count(),
            "total_classes": len(klasses),
            "total_leaves": total_leave,
            "events": events,
            "section": "teacher-dashboard",
            # "total_pass_courses": pass_courses_count,
            # "total_cources_writen": marks.count(),
            # "total_courses": total_courses,
            # "payment_history": payment_history,
            # "class": student.current_class,
            # "class_enrolment": class_enrolment.count(),
        }
        return render(request, template_name, context)
    else:
        messages.error(request, "You are not allowed to be here.")
        return render(
            request, template_name, {"error_message": "You are not allowed to be here."}
        )


def assign_class_to_teacher(request, teacher_pkid, teacher_mat):
    teachers = TeacherProfile.objects.filter(pkid=teacher_pkid, matricule=teacher_mat)
    if teachers.exists():
        teacher = teachers.first()
    else:
        messages.error(request, "Teacher with given matricule, not found..")
        return redirect(reverse("staff:admin-dashboard"))
    # check if ajax was sent
    if request.method == "POST":
        # print("This are the selected subjects", request.body)
        data = json.loads(request.body)

        # get current assigned subject for the given teacher
        assigned_subjects = Subject.objects.filter(assigned_to=teacher)

        print(data)
        # extract all the IDs of the selected subjects and add them to list.
        selected_subjects_ids = []
        for subject in data["selectedSubjects"]:
            print(subject["pkid"])
            selected_subjects_ids.append(subject.get("pkid"))

        if len(selected_subjects_ids) < 1:
            # remove all the subject currently assigned to the teacher
            for sub in assigned_subjects:
                sub.assigned_to = None
                sub.assigned = False
                sub.save()
                return JsonResponse({"message": "updated.."})
        # Flush out all the subjects that exist in the  and reset

        if len(assigned_subjects) > 0 and len(selected_subjects_ids) > 0:
            for subject in assigned_subjects:
                # remove the subject
                subject.assigned_to = None
                subject.assigned = False
                subject.save()

        for pkid in selected_subjects_ids:
            sub = Subject.objects.filter(pkid=pkid).first()
            if sub:
                sub.assigned_to = teacher
                sub.assigned = True
                sub.save()

        return JsonResponse({"message": "updated.."})

    # continue if teacher exists....
    # get all subjects that are assigned to the current teacher
    assigned_subjects = Subject.objects.filter(assigned_to=teacher)
    # get remaining subjects...
    subjects = Subject.objects.filter(assigned=False)

    # compile list of unique subjects
    context = {
        "assigned_subjects": assigned_subjects,
        "subjects": subjects,
        "teacher": teacher,
    }
    template_name = "teachers/assign-subjects.html"
    return render(request, template_name, context)


@login_required
def download_blank_teacher_form(request):
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Draw title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Teacher Information Form")

    # Draw teacher fields
    p.setFont("Helvetica", 12)
    y = height - 100

    fields = [
        "First Name",
        "Last Name",
        "Gender",
        "Phone Number",
        "Date of Birth",
        "Address",
        "Location",
        "Country",
        "Subject",
        "Region of Origin",
        "Division of Origin",
        "Sub Division of Origin",
        "Date of Recruitment into Public Service",
        "Corps",
        "Career Grade",
        "Payroll Grade",
        "Career Category",
        "Payroll Category Solde",
        "Career Index",
        "Payroll Index",
        "Career Echelon",
        "Payroll Echelon",
        "Service",
        "Appointed Structure",
        "Town",
        "Position Rank",
        "Longevity of Post",
        "Longevity in Administration",
        "Appointment Decision Reference",
        "Indemnity Situation",
        "Remark",
    ]

    max_label_width = max(
        [p.stringWidth(field + ":", "Helvetica", 12) for field in fields]
    )
    line_start_x = 50 + max_label_width + 10
    line_length = 300

    for field in fields:
        p.drawString(50, y, f"{field}:")
        p.line(line_start_x, y, line_start_x + line_length, y)
        y -= 20
        if y < 50:  # Check if y is less than the bottom margin
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 50

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="teacher_form.pdf"'
    response.write(pdf)

    return response


@login_required
def download_teacher_list(request):
    pass

def generate_report_card(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report_card.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    # Sample data
    data = {
        "student_name": "John Doe",
        "term_name": "First Term",
        "sessions": [
            {"exam_session": "First Sequence"},
            {"exam_session": "Second Sequence"},
        ],
        "marks": [
            {
                "subject_name": "Mathematics",
                "first_sequence": 15,
                "session2": 12,
                "average": 13.5,
                "coef": 4,
                "MXC": 54,
                "teacher": "Mr. Smith",
                "remark": "Good",
            },
            # Add more subjects here...
        ],
        "student_data": {
            "sequence1_total": 300,
            "sequence2_total": 280,
            "avg_sum": 290,
            "sum_of_coefs": 50,
            "mxc_sum": 1350,
            "term_remark": "Satisfactory",
            "session1_avg": 12.5,
            "session2_avg": 13,
            "term_avg": 13,
            "class_avg": 12,
            "student_rank": 5,
            "class_total": 30,
        },
    }

    # Set up the styles
    styles = getSampleStyleSheet()

    # Title
    elements.append(
        Paragraph(
            f"{data['student_name']} - {data['term_name']} PROGRESS REPORT",
            styles["Title"],
        )
    )
    elements.append(Spacer(1, 12))

    # Table Header
    table_data = [
        [
            "SUBJECT NAME",
            "1st Seq",
            "2nd Seq",
            "AV./20",
            "COEF",
            "M X C",
            "Teacher's Name",
            "Teacher's Remark",
        ]
    ]

    # Table Body
    for mark in data["marks"]:
        row = [
            mark["subject_name"],
            mark["first_sequence"],
            mark["session2"],
            mark["average"],
            mark["coef"],
            mark["MXC"],
            mark["teacher"],
            mark["remark"],
        ]
        table_data.append(row)

    # Add Grand Total and other rows
    table_data.append(
        [
            "GRAND TOTAL:",
            data["student_data"]["sequence1_total"],
            data["student_data"]["sequence2_total"],
            data["student_data"]["avg_sum"],
            data["student_data"]["sum_of_coefs"],
            data["student_data"]["mxc_sum"],
            "",
            data["student_data"]["term_remark"],
        ]
    )

    table_data.append(
        [
            "SEQ. Avg.",
            data["student_data"]["session1_avg"],
            data["student_data"]["session2_avg"],
            "",
            "",
            data["student_data"]["term_avg"],
            "Class Avg.",
            data["student_data"]["class_avg"],
        ]
    )

    table_data.append(
        [
            "CLASS POSITION:",
            "",
            "",
            "",
            "",
            f"N0. {data['student_data']['student_rank']} / {data['student_data']['class_total']}",
            "",
            "",
        ]
    )

    # Create the table
    table = Table(table_data, repeatRows=1)

    # Style the table
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    # Add the table to the elements
    elements.append(table)

    # Footer
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Principal's Remarks: ___________", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph("Class Master's Signature: ___________", styles["Normal"])
    )
    elements.append(Paragraph("Principal's Signature: ___________", styles["Normal"]))

    # Build the PDF
    doc.build(elements)

    return response
