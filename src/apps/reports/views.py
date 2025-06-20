import os
import tempfile
from io import BytesIO
from time import time

import pdfkit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from PyPDF2 import PdfMerger
from xhtml2pdf import pisa

from apps.students.models import (
    Class,
    ClassAcademicRecord,
    Mark,
    StudentProfile,
    Subject,
)
from apps.terms.models import AcademicYear, ExaminationSession, Term

from .class_master_report import ClassMasterReport
from .student_reporting import ClassPerformanceReport
from .utils import calculate_marks, create_student_academic_records


@login_required
def reports(request, *args, **kwargs):
    classes = Class.objects.all()
    template_name = "reports/reports.html"
    students = StudentProfile.objects.all()
    current_year = AcademicYear.objects.get(is_current=True)
    terms = Term.objects.filter(academic_year=current_year)

    context = {
        "section": "reports-area",
        "classes": classes,
        "students": students,
        "terms": terms,
    }

    return render(request, template_name, context)


@login_required
def create_one_report_card(request, *args, **kwargs):

    if request.method == "POST":

        selected_student_id = request.POST.get("selected_student_id")
        selected_term_id = request.POST.get("selected_term_id")
        if not selected_student_id:
            messages.error(request, "Invalid or empty student id")
            return reverse("reporsts:reports")

        # check it term is valid
        if not selected_term_id:
            messages.error(request, "Invalid or missing term ID")
            return redirect(reverse("reports:reports"))

        # Get the student
        student = StudentProfile.objects.filter(pkid=selected_student_id)

        if student.exists():
            student = student.first()
            if len(student.get_all_subjects()) < 1:
                messages.error(request, "No subjects associated to this student.")
                return redirect(reverse("reports:reports"))
        else:
            messages.error(request, "No student with given id and matricule found.")
            return redirect(reverse("reports:reports"))

        #     # current year
        academic_year = AcademicYear.objects.filter(is_current=True).first()
        term = Term.objects.get(pkid=selected_term_id)
        klass = student.current_class

        # Instantiate a performance object
        performance_obj = ClassPerformanceReport(klass.pkid, term.pkid)
        # call the setup function before moving on.

        setup = performance_obj.setup()
        if setup:
            messages.error(request, setup)
            return redirect(reverse("reports:reports"))
        # performance_obj.generate_student_report_data()

        sessions = ExaminationSession.objects.filter(term=term)

        student_marks = performance_obj.generate_student_report_data(student)
        if not student_marks:
            messages.error(request, "Unset terms")
            return redirect(reverse("reports:reports"))
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
        setup = performance_obj.setup()
        if setup:
            messages.error(request, setup)
            return redirect(reverse("reports:reports"))

        # check if class has any subject attatched to it, if not, return.
        if len(performance_obj.sub_dicts) < 1:
            messages.warning(request, "No subjects associated to the given class.")
            return redirect(reverse("reports:reports"))

        if performance_obj.get_total_students_per_class() < 1:
            messages.warning(request, "No students for the given class")
            return redirect(reverse("reports:reports"))

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

            context = {"data": pdf_data}
            print("This is the pdf data", context)
            template_path = "reports/report-card-generation-template.html"
            template = get_template(template_path)
            html = template.render(context)
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            if pisa_status.err:
                return HttpResponse("Error generating PDF")
            pdf_merger.append(BytesIO(pdf_file.getvalue()))
            print("##### doing the thing")
            performance_obj.create_student_academic_records(
                student, student_marks, student_ranking
            )

            pdf_file.seek(0)
        print("############ creating some report cards")
        performance_obj.set_highest_subject_score_to_class()
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{performance_obj.generate_file_name()}-report-cards.pdf"'
        )
        pdf_merger.write(response)

        return response
    else:
        return redirect("reports:reports")


def create_class_master_report(request):

    # get class Id
    if request.method == "POST":
        class_pkid = request.POST.get("selected_class_id")
        term_id = request.POST.get("selected_term_id")

        classes = Class.objects.filter(pkid=class_pkid)
        if classes.exists():
            klass = classes.first()
        else:
            messages.error(request, "Class with given ID could not be found")
            return reverse("reports:reports")
        # term = Term.objects.filter(pkid=term_id)

        # create a class report instance

        cmr = ClassMasterReport(klass.pkid, term_id)
        setup = cmr.setup()
        if setup:
            messages.error(request, setup)
            return redirect(reverse("reports:reports"))
        term = cmr.get_term()
        klass = cmr.get_class()
        context = {
            "total_girls": klass.get_total_girls(),
            "total_boys": klass.get_total_boys(),
            "sum_boys_girls": klass.get_total_enrol(),
            "class": klass,
            "class_avg": ClassAcademicRecord.get_class_avg(term, klass),
            "best_subject": klass.best_subject,
            "worst_subject": klass.worst_subject,
            "boys_passed": cmr.get_total_boys_passed(),
            "girls_passed": cmr.get_total_girls_passed(),
            "highest_avg": cmr.get_highest_student_avg(),
            "lowest_avg": cmr.get_lowest_student_avg(),
            "first_three_students": cmr.get_best_students_from_class(),
            "last_three_students": cmr.get_last_three_studenst(),
            "first": cmr.calculate_grading(0, 5.99),
            "second": cmr.calculate_grading(6, 7.99),
            "third": cmr.calculate_grading(8, 9.99),
            "fourth": cmr.calculate_grading(10, 11.99),
            "fifth": cmr.calculate_grading(12, 13.99),
            "sixth": cmr.calculate_grading(14, 15.99),
            "seventh": cmr.calculate_grading(16, 17.99),
            "eigth": cmr.calculate_grading(18, 20),
            "report_title": cmr.get_report_title(),
        }
        template_name = "reports/classtest.html"
        # context = {"data": pdf_data}
        return render(request, template_name, context)
    else:
        return redirect(reverse("reports:reports"))


def download_class_master_report(request, class_pkid):

    # # get class Id
    # if request.method == "POST":
    # requires more work
    term = Term.objects.get(is_current=True)

    classes = Class.objects.filter(pkid=class_pkid)
    if classes.exists():
        klass = classes.first()
    else:
        messages.error(request, "Class with given ID could not be found")
        return reverse("reports:reports")
    # term = Term.objects.filter(pkid=term_id)
    term = Term.objects.get(is_current=True)

    # create a class report instance

    cmr = ClassMasterReport(klass.pkid, term.pkid)
    pdf_data = {
        "total_girls": klass.get_total_girls(),
        "total_boys": klass.get_total_boys(),
        "sum_boys_girls": klass.get_total_enrol(),
        "class": klass,
        "class_avg": ClassAcademicRecord.get_class_avg(term, klass=klass),
        "best_subject": klass.best_subject,
        "worst_subject": klass.worst_subject,
        "boys_passed": cmr.get_total_boys_passed(),
        "girls_passed": cmr.get_total_girls_passed(),
        "highest_avg": cmr.get_highest_student_avg(),
        "lowest_avg": cmr.get_lowest_student_avg(),
        "first_three_students": cmr.get_best_students_from_class(),
        "last_three_students": cmr.get_last_three_studenst(),
        "first": cmr.calculate_grading(0, 5.99),
        "second": cmr.calculate_grading(6, 7.99),
        "third": cmr.calculate_grading(8, 9.99),
        "fourth": cmr.calculate_grading(10, 11.99),
        "fifth": cmr.calculate_grading(12, 13.99),
        "sixth": cmr.calculate_grading(14, 15.99),
        "seventh": cmr.calculate_grading(16, 17.99),
        "eigth": cmr.calculate_grading(18, 20),
        "report_title": cmr.get_report_title(),
    }
    template_name = "reports/classtest.html"
    context = {"data": pdf_data}

    report_name = f"{klass.get_full_name()}-classmaster-report"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Dispositon"] = f'attachment; filename="{report_name}.pdf"'

    template_path = "reports/class-master.html"

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response
