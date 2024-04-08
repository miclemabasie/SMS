from django.shortcuts import render
import pdfkit
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.students.models import StudentProfile


def reports(request, *args, **kwargs):

    template_name = "reports/reports.html"
    context = {
        "section": "reports",
    }

    return render(request, template_name, context)


def generate_report_card_pdf(request, class_id):
    # Get all students in the class
    students = StudentProfile.objects.filter(class_id=class_id)

    # Create an HttpResponse object with content type PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="class_report_cards.pdf"'

    # Loop through each student and generate their report card
    for student in students:
        # Generate HTML content for the report card
        html_content = render_to_string(
            "report_card_template.html", {"student": student}
        )

        # Convert HTML content to PDF
        pdfkit.from_string(
            html_content, response, options={"quiet": ""}, cover_first=False
        )
        response.write("\x0C")  # Add a page break between report cards

    return response
