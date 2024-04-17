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

from xhtml2pdf import pisa
from django.template.loader import get_template


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


from .utils import calculate_marks


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

        print(calculate_marks(student))
        #     # current year
        academic_year = AcademicYear.objects.filter(is_current=True).first()
        term = Term.objects.filter(is_current=True).first()

        sessions = ExaminationSession.objects.filter(term=term)

        #     # Get the marks for the first sequestn in the term
        #     term_1, term_2 = ExaminationSession.objects.filter(term=term)

        #     print(term_1)
        #     print(term_2)

        #     # marks for term1
        #     sequence_1_marks_list = Mark.objects.filter(student=student, exam_session=term_1)
        #     sequence_2_marks_list = Mark.objects.filter(student=student, exam_session=term_2)

        #     sequence_1_marks = []
        #     for mark in sequence_1_marks_list:
        #         sequence_1_marks.append((mark.subject.name, mark.score))

        #     sequence_2_marks = []
        #     for mark in sequence_2_marks_list:
        #         sequence_2_marks.append((mark.subject.name, mark.score))

        #     print(sequence_1_marks)
        #     print(sequence_2_marks)
        student_marks = calculate_marks(student)
        pdf_data = {
            "marks": student_marks["data"],
            "student_data": student_marks,
            "term": term,
            "term_name": term.term.title(),
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


import pdfkit


@login_required
def generate_report_card_pdf(request):
    if request.method == "POST":
        class_id = request.POST.get("selected_class_id")
        students = StudentProfile.objects.filter(current_class__pkid=class_id)

        # Create a temporary directory to store individual PDF files
        temp_dir = tempfile.mkdtemp()

        # Generate individual PDF files for each student's report card
        for student in students:
            # Generate HTML content for the student's report card
            html_content = render_to_string(
                "reports/report-card-generation-template.html",
                {"student": student},
            )

            # Generate PDF file from HTML content
            pdf_filename = os.path.join(temp_dir, f"{student.id}_report_card.pdf")
            pdfkit.from_string(html_content, pdf_filename)

        # Merge individual PDF files into a single PDF file
        merged_pdf_path = os.path.join(temp_dir, "class_report_cards.pdf")
        pdf_files = [
            os.path.join(temp_dir, f"{student.id}_report_card.pdf")
            for student in students
        ]
        pdf_merger = PdfMerger()
        for pdf_file in pdf_files:
            pdf_merger.append(pdf_file)
        pdf_merger.write(merged_pdf_path)
        pdf_merger.close()

        # Send the merged PDF file as a response for download
        with open(merged_pdf_path, "rb") as merged_pdf_file:
            response = HttpResponse(
                merged_pdf_file.read(), content_type="application/pdf"
            )
            response["Content-Disposition"] = (
                'attachment; filename="class_report_cards.pdf"'
            )
            return response

    else:
        return redirect(reverse("reports:reports"))
