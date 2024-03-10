from django import template
from apps.students.models import StudentProfile

register = template.Library()


@register.simple_tag
def total_students():
    return StudentProfile.objects.count()