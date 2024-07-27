from django import template

register = template.Library()


from apps.terms.models import AcademicYear, ExaminationSession, Term


@register.simple_tag
def current_working_session():
    current_year = AcademicYear.objects.get(is_current=True)
    current_terms = Term.objects.filter(is_current=True, academic_year=current_year)
    if current_terms.exists():
        current_term = current_terms.first()
        info = f"current session: {current_year.name}-{current_term.term}"
        return info
    return "Invalid session-term configuration."
