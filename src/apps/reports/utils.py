from .models import StudentProfile
from apps.students.models import Mark, Subject
from apps.terms.models import Term, AcademicYear, ExaminationSession


def calculate_marks(student):

    # get all subjects for the current student

    subjects = student.get_all_subjects()

    # get the current term
    term = Term.objects.get(is_current=True)

    # get the sessions for the current term
    session1, session2 = ExaminationSession.objects.filter(term=term)

    data = []

    # Go through all the subjects
    session_1_total_marks = 0
    session_2_total_marks = 0
    sum_of_coef = 0
    mxc_total = 0

    for subject in subjects:
        # check if subject has marks

        subject_mark_session1 = Mark.objects.filter(
            subject=subject, exam_session=session1, student=student
        )

        print("first mark", subject_mark_session1)

        if not subject_mark_session1.exists():
            score1 = "/"
        else:
            teacher = subject_mark_session1.first().teacher.user.first_name
            score1 = subject_mark_session1.first().score

        subject_mark_session2 = Mark.objects.filter(
            subject=subject, exam_session=session2, student=student
        )

        print("first mark", subject_mark_session2)

        if not subject_mark_session2.exists():
            score2 = "/"
        else:
            score2 = subject_mark_session2.first().score

        # assign "/" to average if no score is found
        if score1 == "/" or score2 == "/":
            average = "/"
            mxc = "/"
            remark = ""
            teacher = "Admin"
        else:
            average = (score1 + score2) / 2
            mxc = average * subject.coef
            session_1_total_marks += score1 * subject.coef
            session_2_total_marks += score2 * subject.coef
            mxc_total += mxc

            if mxc < 50:
                remark = "V. poor"
            elif mxc < 70:
                remark = "Good"
            elif mxc < 80:
                remark = "V. Good"
            else:
                remark = "Excellent"
            teacher = teacher

        sum_of_coef += subject.coef

        data.append(
            {
                "subject_name": subject.name,
                "first_sequence": score1,
                "session2": score2,
                "average": average,
                "coef": subject.coef,
                "MXC": mxc,
                "teacher": teacher,
                "remark": remark,
            }
        )

    avg_sum = (session_1_total_marks + session_2_total_marks) / 2

    # calculate first_sequence avg
    session_1_avg = session_1_total_marks / sum_of_coef
    session_2_avg = session_2_total_marks / sum_of_coef
    term_avg = mxc_total / sum_of_coef

    if term_avg < 5:
        term_remark = "V. Poor"

    elif term_avg < 10:
        term_remark = "Poor"
    elif term_avg < 13:
        term_remark = "Good"
    elif term_avg < 18:
        term_remark = "V. Good"
    else:
        term_remark = "Excellent"

    student_data = {
        "data": data,
        "sum_of_coefs": sum_of_coef,
        "sequence1_total": session_1_total_marks,
        "sequence2_total": session_2_total_marks,
        "avg_sum": avg_sum,
        "mxc_sum": mxc_total,
        # avg data
        "session1_avg": round(session_1_avg, 2),
        "session2_avg": round(session_2_avg, 2),
        "term_avg": round(term_avg, 2),
        "term_remark": term_remark,
    }
    return student_data


[
    {
        "subject_name": "this is the update name",
        "first_sequence": "/",
        "session2": "/",
        "average": "/",
        "coef": 5,
        "MXC": "/",
        "teacher": "Admin",
        "remark": "",
    },
    {
        "subject_name": "Ripple",
        "first_sequence": "/",
        "session2": "/",
        "average": "/",
        "coef": 1,
        "MXC": "/",
        "teacher": "Admin",
        "remark": "",
    },
    {
        "subject_name": "Civics",
        "first_sequence": 1,
        "session2": 1,
        "average": 1.0,
        "coef": 2,
        "MXC": 2.0,
        "teacher": "Erica",
        "remark": "V. poor",
    },
    {
        "subject_name": "Cardano",
        "first_sequence": "/",
        "session2": "/",
        "average": "/",
        "coef": 1,
        "MXC": "/",
        "teacher": "Admin",
        "remark": "",
    },
    {
        "subject_name": "Maths",
        "first_sequence": 12,
        "session2": 20,
        "average": 16.0,
        "coef": 5,
        "MXC": 80.0,
        "teacher": "Erica",
        "remark": "Excellent",
    },
    {
        "subject_name": "Bitcoin",
        "first_sequence": "/",
        "session2": "/",
        "average": "/",
        "coef": 1,
        "MXC": "/",
        "teacher": "Admin",
        "remark": "",
    },
    {
        "subject_name": "Namecoin",
        "first_sequence": "/",
        "session2": "/",
        "average": "/",
        "coef": 1,
        "MXC": "/",
        "teacher": "Admin",
        "remark": "",
    },
    {
        "subject_name": "Emercoin",
        "first_sequence": "/",
        "session2": "/",
        "average": "/",
        "coef": 1,
        "MXC": "/",
        "teacher": "Admin",
        "remark": "",
    },
]
