from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def generate_report_card_pdf(request):
    # Fake student data
    student = {
        "first_name": "John",
        "last_name": "Doe",
        "section": "Science",
        "specialty": "Mathematics",
        "date_of_birth": "01/01/2000",
        "academic_year": "2023/2024",
        "class": "Form 4",
        "repeater": "No",
        "adm_nr": "12345",
        "term": "First Term",
        "subjects": [
            {
                "name": "Mathematics",
                "seq1": 15,
                "seq2": 14,
                "average": 14.5,
                "coef": 4,
                "mx_c": 58,
                "teacher": "Mr. Smith",
                "remark": "V. Good",
                "signature": "",
            },
            {
                "name": "English",
                "seq1": 13,
                "seq2": 12,
                "average": 12.5,
                "coef": 3,
                "mx_c": 37.5,
                "teacher": "Ms. Johnson",
                "remark": "Good",
                "signature": "",
            },
            {
                "name": "History",
                "seq1": 9,
                "seq2": 11,
                "average": 10,
                "coef": 2,
                "mx_c": 20,
                "teacher": "Mr. Lee",
                "remark": "Poor",
                "signature": "",
            },
        ],
        "grand_total": {
            "total": 37,
            "coef": 9,
            "mx_c": 115.5,
            "remark": "Good progress overall",
        },
        "seq_avg": {
            "avg": 12.33,
            "term": "Term 1",
            "class_avg": 12.5,
            "position": "No. 5 / 30",
        },
        "class_level": "Good",
        "total_enrollment": 30,
    }

    # Generate PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report_card.pdf"'

    # Create canvas
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 30, f"{student['term']} Progress Report")

    # Student info section
    p.setFont("Helvetica", 12)
    info_x = 5
    info_y = height - 80
    p.drawString(info_x, info_y, f"Section: {student['section']}")
    p.drawString(info_x, info_y - 20, f"Specialty: {student['specialty']}")
    p.drawString(
        info_x,
        info_y - 40,
        f"Student's Name: {student['first_name']} {student['last_name']}",
    )
    p.drawString(info_x, info_y - 60, f"Date of Birth: {student['date_of_birth']}")
    p.drawString(info_x + 250, info_y, f"Academic Year: {student['academic_year']}")
    p.drawString(info_x + 250, info_y - 20, f"Class: {student['class']}")
    p.drawString(info_x + 250, info_y - 40, f"Repeater: {student['repeater']}")
    p.drawString(info_x + 250, info_y - 60, f"Adm. Nr: {student['adm_nr']}")

    # Subjects table
    subjects_data = [
        [
            "SUBJECT NAME",
            "1st Seq",
            "2nd Seq",
            "AV./20",
            "COEF",
            "M X C",
            "Teacher",
            "Remark",
            "Signature",
        ]
    ]
    for subject in student["subjects"]:
        subjects_data.append(
            [
                subject["name"],
                str(subject["seq1"]),
                str(subject["seq2"]),
                str(subject["average"]),
                str(subject["coef"]),
                str(subject["mx_c"]),
                subject["teacher"],
                subject["remark"],
                subject["signature"],
            ]
        )

    subjects_table = Table(
        subjects_data, colWidths=[100, 40, 40, 50, 40, 50, 100, 80, 80]
    )
    subjects_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    subjects_table.wrapOn(p, width - 100, height)
    subjects_table.drawOn(p, 5, info_y - 120)

    # Grand Total, Seq. Avg., Class Level, and Total Enrollment section
    other_info_data = [
        [
            "GRAND TOTAL:",
            "",
            "",
            "",
            str(student["grand_total"]["coef"]),
            str(student["grand_total"]["mx_c"]),
            "",
            "",
            student["grand_total"]["remark"],
        ],
        [
            "SEQ. Avg.",
            "",
            "",
            f"{student['seq_avg']['term']}",
            "",
            f"{student['seq_avg']['avg']}",
            "Class Avg.",
            f"{student['seq_avg']['class_avg']}",
            "",
        ],
        [
            "",
            "",
            "",
            "CLASS POSITION:",
            "",
            f"{student['seq_avg']['position']}",
            "",
            "",
            "",
        ],
        ["CLASS LEVEL", "", "", "", "", "", "", "", f"{student['class_level']}"],
        [
            "TOTAL ENROLLMENT:",
            "",
            "",
            "",
            "",
            f"{student['total_enrollment']}",
            "",
            "",
            "",
        ],
    ]

    other_info_table = Table(
        other_info_data, colWidths=[120, 40, 40, 70, 40, 50, 100, 100, 100]
    )
    other_info_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    other_info_table.wrapOn(p, width - 100, height)
    other_info_table.drawOn(p, 5, info_y - 300)

    # Principal's Remarks
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, info_y - 400, "Principal's Remarks")
    p.drawString(
        50,
        info_y - 420,
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget mi et leo iaculis",
    )
    p.drawString(50, info_y - 440, "bibendum nec sed felis.")

    # Signatures
    p.setFont("Helvetica", 12)
    p.drawString(50, info_y - 500, "Signature of the class master:")
    p.drawString(250, info_y - 500, "Signature of the principal:")

    p.showPage()
    p.save()

    return response


from django.shortcuts import render
from django.http import JsonResponse
from apps.students.models import StudentProfile


def student_report_data(request):
    # Fetch data from your Student model or any other relevant model
    students = (
        StudentProfile.objects.all()
    )  # Adjust this query based on your actual models

    # Prepare the data in a JSON-friendly format
    student_data = []
    for student in students:
        # Example structure, adjust as per your actual data model
        student_info = {
            "name": student.user.username,
            "section": "Industrial",
            "specialty": "F4",
            "date_of_birth": student.user.dob.strftime(
                "%Y-%m-%d"
            ),  # Example date formatting
            "academic_year": "2024-2025",
            "class": "Form 1 A",
            "repeater": student.is_repeater,
            "adm_nr": student.matricule,
            "subjects": [
                {
                    "name": "Mathematics",
                    "seq1": 15,
                    "seq2": 14,
                    "average": 14.5,
                    "coef": 4,
                    "mx_c": 58,
                    "teacher": "Mr. Smith",
                    "remark": "Good progress",
                    "signature": "Signature",
                },
                {
                    "name": "English",
                    "seq1": 13,
                    "seq2": 12,
                    "average": 12.5,
                    "coef": 3,
                    "mx_c": 37.5,
                    "teacher": "Ms. Johnson",
                    "remark": "Well done",
                    "signature": "Signature",
                },
                {
                    "name": "History",
                    "seq1": 9,
                    "seq2": 11,
                    "average": 10,
                    "coef": 2,
                    "mx_c": 20,
                    "teacher": "Mr. Lee",
                    "remark": "Needs improvement",
                    "signature": "Signature",
                },
            ],
            "grand_total": {
                "total": 37,
                "coef": 9,
                "mx_c": 115.5,
                "remark": "Good progress overall",
            },
            "seq_avg": {
                "avg": 12.33,
                "term": "Term 1",
                "class_avg": 12.5,
                "position": "No. 5 / 30",
            },
            "class_level": "Good",
            "total_enrollment": 30,
        }
        student_data.append(student_info)

    # Return JSON response
    return JsonResponse(student_data, safe=False)


def test_report(request):
    template_name = "reports/gpt-report-design.html"
    context = {}
    return render(request, template_name, context)