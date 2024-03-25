from .models import StudentProfile


def check_student_is_owing(student_pkid):
    student = StudentProfile.objects.get(pkid=student_pkid)
    if student.is_owing:
        return "Yes"
    else:
        return "No"


def check_student_is_repeater(student_pkid):
    student = StudentProfile.objects.get(pkid=student_pkid)
    if student.is_repeater:
        return "Yes"
    else:
        return "No"
