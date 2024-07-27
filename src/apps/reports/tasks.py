import logging
import os
from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.loader import get_template
from pypdf import PdfMerger
from weasyprint import HTML

from apps.reports.models import ReportGenerationStatus
from apps.reports.student_reporting import ClassPerformanceReport
from apps.settings.models import Setting
from apps.students.models import StudentProfile
from apps.terms.models import AcademicYear, ExaminationSession, Term

# Set up logging
logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_and_store_class_report_cards(self, class_id, term_id):
    performance_obj = ClassPerformanceReport(class_id, term_id)
    setup = performance_obj.setup()
    if setup:
        return setup

    # Check if the class has subjects and students
    if len(performance_obj.sub_dicts) < 1:
        return "No subjects associated with the given class."
    if performance_obj.get_total_students_per_class() < 1:
        return "No students for the given class."

    students = performance_obj.get_all_students_for_current_class()
    academic_year = AcademicYear.objects.filter(is_current=True).first()
    term = performance_obj.get_term()
    sessions = ExaminationSession.objects.filter(term=term)
    class_performance_data = performance_obj.generate_performacne_rank_list()
    class_performance = class_performance_data["class_performance"]
    class_avg = performance_obj.get_class_avg()
    setting = Setting.objects.all().first()

    # Initialize PdfMerger to combine PDFs
    pdf_merger = PdfMerger()
    file_paths = []
    for student in students:
        student_marks = performance_obj.generate_student_report_data(student)
        student_ranking = performance_obj.get_student_rank(student, class_performance)

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
            "setting": setting,
            "student": student,
            "class": performance_obj.get_class(),
            "first_term_avg": "",
            "second_term_avg": "",
            "annual_avg": "8",
            "promotion_decision": "Repeat",
        }

        # Determine the template path based on the term
        if performance_obj.is_first_term():
            template_path = "reports/first_term_report_card.html"
        elif performance_obj.is_second_term():
            first_term_avg = performance_obj.get_first_term_report_data(student)
            pdf_data["first_term_avg"] = first_term_avg
            template_path = "reports/second_term_report_card.html"
        elif performance_obj.is_third_term():
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
        template = get_template(template_path)
        html = template.render(context)

        pdf_file = BytesIO()
        HTML(string=html).write_pdf(pdf_file)
        pdf_file.seek(0)

        # Save PDF to a file
        file_name = f"{student.matricule}_report_card.pdf"
        report_file = ContentFile(pdf_file.getvalue(), file_name)
        relative_path = f"reports/{file_name}"
        try:
            file_path = default_storage.save(relative_path, report_file)
            absolute_path = default_storage.path(file_path)
            if not os.path.isfile(absolute_path):
                logger.error(f"File not found after saving: {absolute_path}")
                continue
            file_paths.append(absolute_path)  # Keep track of file paths
        except Exception as e:
            logger.error(f"Error saving file {file_name}: {e}")
            continue

        # Append to the PDF merger
        try:
            pdf_merger.append(absolute_path)
            logger.info(f"Successfully appended file: {absolute_path}")
        except Exception as e:
            logger.error(f"Failed to append file {absolute_path}: {e}")
            continue

        pdf_file.close()
        performance_obj.create_student_academic_records(
            student, student_marks, student_ranking
        )
        logger.info(f"Generating report for student: {student}")

    # Finalize and serve the merged PDF
    merged_pdf_file = BytesIO()
    try:
        pdf_merger.write(merged_pdf_file)
        merged_pdf_file.seek(0)

        merged_file_name = (
            f"{performance_obj.get_class().get_class_name}_report_cards.pdf"
        )
        merged_report_file = ContentFile(merged_pdf_file.getvalue(), merged_file_name)
        merged_file_path = default_storage.save(
            f"reports/{merged_file_name}", merged_report_file
        )
        logger.info(f"Successfully saved merged PDF to: {merged_file_path}")
    except Exception as e:
        logger.error(f"Failed to create merged PDF: {e}")
        return "Failed to generate merged report cards."
    finally:
        merged_pdf_file.close()

        # Delete individual report files
    for file_path in file_paths:
        try:
            os.remove(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")

        # Update the report generation status
    try:
        report = ReportGenerationStatus.objects.get(task_id=self.request.id)
        report.status = "Completed"
        report.klass = performance_obj.get_class()
        report.file_path = merged_file_path
        report.save()
        logger.info(f"Report status updated with file path: {merged_file_path}")
    except ReportGenerationStatus.DoesNotExist:
        logger.error(
            f"ReportGenerationStatus with task_id {self.request.id} not found."
        )
    except Exception as e:
        logger.error(f"Failed to update report status: {e}")
    return merged_file_path


# @shared_taks
# def
