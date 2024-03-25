from django import template

register = template.Library()


from apps.terms.models import AcademicYear, Term, ExaminationSession


@register.simple_tag
def current_working_session():
    current_year = AcademicYear.objects.get(is_current=True)
    current_term = Term.objects.get(is_current=True)
    current_exam_session = ExaminationSession.objects.get(is_current=True)
    info = (
        f"{current_year.name}-{current_term.term}-{current_exam_session.exam_session}"
    )
    return info
