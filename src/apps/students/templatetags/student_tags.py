from django import template

from apps.students.models import StudentProfile
from apps.terms.models import AcademicYear, ExaminationSession, Term

register = template.Library()

# print("This is the tags file")


@register.simple_tag
def current_working_session():
    # current_year = AcademicYear.objects.get(is_current=True)
    # current_term = Term.objects.get(is_current=True)
    # current_exam_session = ExaminationSession.objects.get(is_current=True)
    # info = f"Year: {current_year.name}-{current_term.term}-{current_exam_session.exam_session}"
    # print("This is the same infor message: ", info)
    return "info"


# @register.simple_tag
# def total_students():
#     return "HI"
#     return StudentProfile.objects.all().count()
