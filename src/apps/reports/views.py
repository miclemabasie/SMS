from django.shortcuts import render, redirect
from django.urls import reverse
import pdfkit
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.students.models import StudentProfile, Class, Subject

import tempfile
from PyPDF2 import PdfMerger
import os


def reports(request, *args, **kwargs):
    classes = Class.objects.all()
    template_name = "reports/reports.html"
    context = {"section": "reports", "classes": classes}

    return render(request, template_name, context)


import pdfkit


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
