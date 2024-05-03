from django.shortcuts import render, redirect
from django.urls import reverse
import pdfkit
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.students.models import StudentProfile, Class, Subject, Mark
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.terms.models import AcademicYear, Term, ExaminationSession

import tempfile
from PyPDF2 import PdfMerger
import os
from .utils import calculate_marks, create_student_academic_records
from .student_reporting import ClassPerformanceReport

from io import BytesIO

from xhtml2pdf import pisa
from django.template.loader import get_template
from time import time


@login_required
def reports(request, *args, **kwargs):
    classes = Class.objects.all()
    template_name = "reports/reports.html"
    students = StudentProfile.objects.all()

    context = {
        "section": "reports",
        "classes": classes,
        "students": students,
    }

    return render(request, template_name, context)


@login_required
def create_one_report_card(request, *args, **kwargs):

    if request.method == "POST":

        selected_student_id = request.POST.get("selected_student_id")
        if not selected_student_id:
            messages.error(request, "Invalid or empty student id")
            return reverse("reporsts:reports")
        # Get the student
        student = StudentProfile.objects.filter(pkid=selected_student_id)

        if student.exists():
            student = student.first()
        else:
            messages.error(request, "No student with given id and matricule found.")
            return redirect(reverse("reports:reports"))

        #     # current year
        academic_year = AcademicYear.objects.filter(is_current=True).first()
        term = Term.objects.filter(is_current=True).first()
        klass = student.current_class

        # Instantiate a performance object
        performance_obj = ClassPerformanceReport(klass.pkid, term.pkid)

        # performance_obj.generate_student_report_data()

        sessions = ExaminationSession.objects.filter(term=term)

        student_marks = performance_obj.generate_student_report_data(student)
        pdf_data = {
            "marks": student_marks["data"],
            "student_data": student_marks,
            "term": term,
            "term_name": term.term.upper(),
            "sessions": sessions,
            "year": academic_year,
        }
        context = {"data": pdf_data}

        report_card_name = f"{student.user.first_name}-report"
        response = HttpResponse(content_type="application/pdf")

        template_path = "reports/report-card-generation-template.html"

        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")
        return response
    else:
        return redirect(reverse("reports:reports"))


@login_required
def create_report_cards(request):
    if request.method == "POST":
        selected_class_id = request.POST.get("selected_class_id")

        # get class

        classes = Class.objects.filter(pkid=selected_class_id)
        term = Term.objects.get(is_current=True)

        performance_obj = ClassPerformanceReport(selected_class_id, term.pkid)

        # Get all students for the class
        students = performance_obj.get_all_students_for_current_class()

        academic_year = AcademicYear.objects.filter(is_current=True).first()
        # get the current term
        term = performance_obj.get_term()

        sessions = ExaminationSession.objects.filter(term=term)

        # Initialize a BytesIO object to write PDF content
        pdf_file = BytesIO()
        pdf_merger = PdfMerger()

        class_performance_data = performance_obj.generate_performacne_rank_list()
        # total_avgs = class_performance_data["total_avg"]
        class_performance = class_performance_data["class_performance"]

        # calculate class avg
        class_avg = performance_obj.get_class_avg()

        for student in students:
            student_marks = performance_obj.generate_student_report_data(student)
            student_ranking = performance_obj.get_student_rank(
                student, class_performance
            )

            print(student_marks)

            pdf_data = {
                "marks": student_marks["data"],
                "student_data": student_marks,
                "term": term,
                "term_name": term.term.upper(),
                "sessions": sessions,
                "year": academic_year,
                "student_rank": student_ranking,
                "class_total": len(students),
                "class_avg": class_avg,
            }
            print("starting to write pdf")
            context = {"data": pdf_data}
            template_path = "reports/report-card-generation-template.html"
            template = get_template(template_path)
            html = template.render(context)
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            if pisa_status.err:
                return HttpResponse("Error generating PDF")
            pdf_merger.append(BytesIO(pdf_file.getvalue()))
            performance_obj.create_student_academic_records(
                student, student_marks, student_ranking
            )
            pdf_file.seek(0)
            print("end write")

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{performance_obj.generate_file_name()}-report-cards.pdf"'
        )
        pdf_merger.write(response)

        return response
    else:
        return redirect("reports:reports")

# @login_required
# def create_report_cards(request):
#     if request.method == "POST":
#         ftime = time()
#         selected_class_id = request.POST.get("selected_class_id")

#         # get class

#         classes = Class.objects.filter(pkid=selected_class_id)
#         term = Term.objects.get(is_current=True)

#         if classes.exists():
#             klass = classes.first()
#         else:
#             messages.error(request, "No class found with given id.")
#             return redirect(reverse("reports:reports"))

#         # Get all students for the class
#         students = StudentProfile.objects.filter(current_class=klass)

#         academic_year = AcademicYear.objects.filter(is_current=True).first()
#         # get the current term
#         term = Term.objects.filter(is_current=True).first()

#         sessions = ExaminationSession.objects.filter(term=term)

#         # Initialize a BytesIO object to write PDF content
#         pdf_file = BytesIO()
#         pdf_merger = PdfMerger()
#         total_avgs = 0
#         class_performance = []
#         for s in students:
#             s_marks = calculate_marks(s)["term_avg"]
#             total_avgs += s_marks
#             class_performance.append((s, s_marks))

#         class_performance = sorted(
#             class_performance,
#             key=lambda x: x[1],
#             reverse=True,
#         )

#         # calculate class avg
#         class_avg = (total_avgs * 20) / (len(students) * 20)

#         for student in students:
#             student_marks = calculate_marks(student)
#             student_ranking = [
#                 rank + 1
#                 for rank, (s, _) in enumerate(class_performance)
#                 if s.pkid == student.pkid
#             ][0]

#             print("marks ", student_marks)

#             # call the method to save the student report data to the database

#             pdf_data = {
#                 "marks": student_marks["data"],
#                 "student_data": student_marks,
#                 "term": term,
#                 "term_name": term.term.upper(),
#                 "sessions": sessions,
#                 "year": academic_year,
#                 "student_rank": student_ranking,
#                 "class_total": len(students),
#                 "class_avg": round(class_avg, 2),
#             }
#             context = {"data": pdf_data}
#             template_path = "reports/report-card-generation-template.html"
#             template = get_template(template_path)
#             html = template.render(context)
#             pisa_status = pisa.CreatePDF(html, dest=pdf_file)
#             if pisa_status.err:
#                 return HttpResponse("Error generating PDF")
#             pdf_merger.append(BytesIO(pdf_file.getvalue()))
#             pdf_file.seek(0)

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = (
#             f'attachment; filename="{klass.grade_level}-{klass.class_name}-report-cards.pdf"'
#         )
#         pdf_merger.write(response)
#         ltime = time()
#         print(f"Time taken is: {ltime - ftime}")

#         return response
#     else:
#         return redirect("reports:reports")
