from django import template
import os
from django.conf import settings
from django.utils.safestring import mark_safe
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


import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="check_image_exists")
def check_image_exists(image_url):
    # Remove the MEDIA_URL from the image_url if it's there
    image_path = image_url.replace(settings.MEDIA_URL, "") if image_url else ""

    # Build the full path to the image file
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

    # Check if the file exists
    if os.path.exists(full_image_path):
        return image_url
    else:
        # Return the path to the default image
        return mark_safe(f"{settings.STATIC_URL}profile_default.png")


# @register.simple_tag
# def total_students():
#     return "HI"
#     return StudentProfile.objects.all().count()
