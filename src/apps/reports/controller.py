from io import BytesIO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import HttpResponse, redirect, reverse, render
from django.template.loader import get_template
from pypdf import PdfMerger
from weasyprint import HTML

from apps.reports.student_reporting import ClassPerformanceReport
from apps.settings.models import Setting
from apps.students.models import Class, StudentProfile
from apps.terms.models import AcademicYear, ExaminationSession, Term

from .models import ReportGenerationStatus  # Example model to track report generation
from .tasks import generate_and_store_class_report_cards


@login_required
def create_report_cards(request):
    if request.method == "POST":
        selected_class_id = request.POST.get("selected_class_id")
        selected_term_id = request.POST.get("selected_term_id")

        if not selected_class_id or not selected_term_id:
            messages.error(request, "Invalid class or term ID.")
            return redirect(reverse("reports:reports"))

        report = ReportGenerationStatus.objects.create(status="pending")
        # Trigger Celery task
        task = generate_and_store_class_report_cards.delay(
            selected_class_id, selected_term_id
        )
        report.status = "Started"
        report.task_id = task.id

        report.save()

        # Optionally, store the task ID and status

        messages.success(
            request,
            "Report generation in progress. You will be notified when it's ready.",
        )
        return redirect(reverse("reports:reports"))

    return redirect(reverse("reports:reports"))


@login_required
def create_one_report_card(request, student_pkid, *args, **kwargs):

    if request.method == "POST":

        selected_student_id = student_pkid
        selected_term_id = request.POST.get("selected_term_id")
        if not selected_student_id:
            messages.error(request, "Invalid or empty student ID")
            return redirect(
                reverse(
                    "students:student-detail",
                    kwargs={"pkid": student.pkid, "matricule": student.matricule},
                )
            )

        if not selected_term_id:
            messages.error(request, "Invalid or missing term ID")
            return redirect(
                reverse(
                    "students:student-detail",
                    kwargs={"pkid": student.pkid, "matricule": student.matricule},
                )
            )

        # Get the student
        student = StudentProfile.objects.filter(pkid=selected_student_id).first()
        if not student:
            messages.error(request, "No student with the given ID found.")
            return redirect(
                reverse(
                    "students:student-detail",
                    kwargs={"pkid": student.pkid, "matricule": student.matricule},
                )
            )

        if len(student.get_all_subjects()) < 1:
            messages.error(request, "No subjects associated with this student.")
            return redirect(
                reverse(
                    "students:student-detail",
                    kwargs={"pkid": student.pkid, "matricule": student.matricule},
                )
            )

        # Get the current year and term
        academic_year = AcademicYear.objects.filter(is_current=True).first()
        term = Term.objects.get(pkid=selected_term_id)
        klass = student.current_class

        # Instantiate a performance object
        performance_obj = ClassPerformanceReport(klass.pkid, term.pkid)
        setup = performance_obj.setup()
        if setup:
            messages.error(request, setup)
            return redirect(
                reverse(
                    "students:student-detail",
                    kwargs={"pkid": student.pkid, "matricule": student.matricule},
                )
            )

        sessions = ExaminationSession.objects.filter(term=term)

        # Generate student report data
        student_marks = performance_obj.generate_student_report_data(student)
        if not student_marks:
            messages.error(request, "Unset terms")
            return redirect(
                reverse(
                    "students:student-detail",
                    kwargs={"pkid": student.pkid, "matricule": student.matricule},
                )
            )

        class_performance_data = performance_obj.generate_performacne_rank_list()
        class_performance = class_performance_data["class_performance"]
        student_ranking = performance_obj.get_student_rank(student, class_performance)
        class_avg = performance_obj.get_class_avg()
        setting = Setting.objects.all().first()

        # Prepare the context data
        pdf_data = {
            "marks": student_marks["data"],
            "student_data": student_marks,
            "term": term,
            "term_name": term.term.upper(),
            "sessions": sessions,
            "year": academic_year,
            "student_rank": student_ranking,
            "class_total": performance_obj.get_total_students_per_class(),
            "class_avg": class_avg,
            "setting": setting,
            "student": student,
            "class": performance_obj.get_class(),
            "first_term_avg": "",
            "second_term_avg": "",
            "annual_avg": "8",
            "promotion_decision": "Repeat",
        }
        # check if the term is first term
        if performance_obj.is_first_term():
            template_path = "reports/first_term_report_card.html"
        elif performance_obj.is_second_term():
            # get the first term report avg and attatch the report card data
            first_term_avg = performance_obj.get_first_term_report_data(student)
            pdf_data["first_term_avg"] = first_term_avg
            template_path = "reports/second_term_report_card.html"
        elif performance_obj.is_third_term():
            # get the data for first and second term and attach to the report
            first_term_avg = performance_obj.get_first_term_report_data(student)
            second_term_avg = performance_obj.get_second_term_report_date(student)
            annual_avg = performance_obj.get_annual_avg(
                student_marks["term_avg"], student
            )
            promotion_decision = performance_obj.get_promotion_decision(
                student, annual_avg
            )
            pdf_data["first_term_avg"] = first_term_avg
            pdf_data["second_term_avg"] = second_term_avg
            pdf_data["annual_avg"] = annual_avg
            pdf_data["promotion_decision"] = promotion_decision
            template_path = "reports/third_term_report_card.html"

            context = {"data": pdf_data}
        context = {"data": pdf_data}
        template = get_template(template_path)
        html = template.render(context)

        pdf_file = BytesIO()
        HTML(string=html).write_pdf(pdf_file)
        pdf_file.seek(0)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{performance_obj.get_single_report_name(student)}-report.pdf"'
        )
        response.write(pdf_file.getvalue())
        pdf_file.close()

        return response

    else:
        return redirect(reverse("reports:reports"))


def download_report(request, file_name):
    file_path = f"reports/{file_name}"
    if default_storage.exists(file_path):
        file = default_storage.open(file_path)
        response = HttpResponse(file.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
    else:
        return HttpResponse("File not found", status=404)


def view_reports(request):
    #
    # Optionally, fetch report generation statuses if using a status model
    report_statuses = ReportGenerationStatus.objects.order_by('-created_at')[:3]

    context = {
        "report_statuses": report_statuses,
    }

    return render(request, "reports/download-reports.html", context)


# kept for just in case...
# @login_required
# def create_report_cards(request):
#     if request.method == "POST":
#         selected_class_id = request.POST.get("selected_class_id")
#         selected_term_id = request.POST.get("selected_term_id")

#         performance_obj = ClassPerformanceReport(selected_class_id, selected_term_id)

#         setup = performance_obj.setup()
#         if setup:
#             messages.error(request, setup)
#             return redirect(reverse("reports:reports"))

#         # check if class has any subject attached to it, if not, return.
#         if len(performance_obj.sub_dicts) < 1:
#             messages.warning(request, "No subjects associated with the given class.")
#             return redirect(reverse("reports:reports"))

#         if performance_obj.get_total_students_per_class() < 1:
#             messages.warning(request, "No students for the given class.")
#             return redirect(reverse("reports:reports"))

#         # Get all students for the class
#         students = performance_obj.get_all_students_for_current_class()

#         academic_year = AcademicYear.objects.filter(is_current=True).first()
#         term = performance_obj.get_term()
#         sessions = ExaminationSession.objects.filter(term=term)

#         # Initialize a PdfMerger object to merge all PDFs
#         pdf_merger = PdfMerger()

#         class_performance_data = performance_obj.generate_performacne_rank_list()
#         class_performance = class_performance_data["class_performance"]

#         class_avg = performance_obj.get_class_avg()
#         setting = Setting.objects.all().first()

#         for student in students:
#             student_marks = performance_obj.generate_student_report_data(student)
#             student_ranking = performance_obj.get_student_rank(
#                 student, class_performance
#             )

#             pdf_data = {
#                 "marks": student_marks["data"],
#                 "student_data": student_marks,
#                 "term": term,
#                 "term_name": term.term.upper(),
#                 "sessions": sessions,
#                 "year": academic_year,
#                 "student_rank": student_ranking,
#                 "class_total": len(students),
#                 "class_avg": class_avg,
#                 "setting": setting,
#                 "student": student,
#                 "class": performance_obj.get_class(),
#                 "first_term_avg": "",
#                 "second_term_avg": "",
#                 "annual_avg": "8",
#                 "promotion_decision": "Repeat",
#             }
#             # check if the term is first term
#             if performance_obj.is_first_term():
#                 template_path = "reports/first_term_report_card.html"
#             elif performance_obj.is_second_term():
#                 # get the first term report avg and attatch the report card data
#                 first_term_avg = performance_obj.get_first_term_report_data(student)
#                 pdf_data["first_term_avg"] = first_term_avg
#                 template_path = "reports/second_term_report_card.html"
#             elif performance_obj.is_third_term():
#                 # get the data for first and second term and attach to the report
#                 first_term_avg = performance_obj.get_first_term_report_data(student)
#                 second_term_avg = performance_obj.get_second_term_report_date(student)
#                 annual_avg = performance_obj.get_annual_avg(
#                     student_marks["term_avg"], student
#                 )
#                 promotion_decision = performance_obj.get_promotion_decision(
#                     student, annual_avg
#                 )
#                 pdf_data["first_term_avg"] = first_term_avg
#                 pdf_data["second_term_avg"] = second_term_avg
#                 pdf_data["annual_avg"] = annual_avg
#                 pdf_data["promotion_decision"] = promotion_decision
#                 template_path = "reports/third_term_report_card.html"

#             context = {"data": pdf_data}
#             template = get_template(template_path)
#             html = template.render(context)

#             # Generate PDF for current student
#             pdf_file = BytesIO()
#             HTML(string=html, base_url="base_url").write_pdf(pdf_file)
#             pdf_file.seek(0)

#             # Append current student's PDF to the PdfMerger object
#             pdf_merger.append(pdf_file)

#             # Reset pdf_file to write a new PDF for the next student
#             pdf_file.close()

#             performance_obj.create_student_academic_records(
#                 student, student_marks, student_ranking
#             )

#         # Finalize the merged PDF and serve as the response
#         performance_obj.set_highest_subject_score_to_class()
#         performance_obj.create_class_report_data(
#             performance_obj.get_class(), term, class_avg
#         )
#         merged_pdf_file = BytesIO()
#         pdf_merger.write(merged_pdf_file)
#         merged_pdf_file.seek(0)

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = (
#             f'attachment; filename="{performance_obj.generate_file_name()}-report-cards.pdf"'
#         )
#         response.write(merged_pdf_file.getvalue())
#         merged_pdf_file.close()

#         return response

#     else:
#         return redirect("reports:reports")
