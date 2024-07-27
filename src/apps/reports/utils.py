from django.contrib import messages
from django.http import HttpResponse

from apps.students.models import Class, Mark, Subject
from apps.terms.models import AcademicYear, ExaminationSession, Term

from .models import AcademicRecord, StudentProfile


def create_student_academic_records(term, student, data, rank, klass):
    """
    Create and save a student academic record after all the marks have been calculated.
    """
    academic_record = AcademicRecord.objects.create(
        student=student,
        exam_term=term,
        total_marks_obtained=data["mxc_sum"],
        student_rank=rank,
        term_avg=data["term_avg"],
        klass=klass,
        session_1_avg=data["session1_avg"],
        session_2_avg=data["session1_avg"],
    )
    try:
        academic_record.save()
        return True
    except Exception as e:
        return f"Error saving student records due to the following error \n {e}"


class PerformStudentReportAnalysis:

    def __init__(self, class_id, term_id):
        self.__class_id = class_id
        self.__term_id = term_id
        self.data = []

    def get_class(self):
        klasses = Class.objects.filter(pkid=self.__class_id)
        if klasses.exists():
            klass = klasses.first()
            return klass
        else:
            return None

    def get_student(self, student_id):
        students = StudentProfile.objects.filter(pkid=student_id)
        if students.exists():
            student = students.first()
            return student
        else:
            return HttpResponse("No student found with given ID.")

    def get_all_subjects_for_a_given_student(student):
        subjects = student.get_all_subjects()
        return subjects

    def get_term(self):
        # get the term
        terms = Term.objects.filter(pkid=self.__term_id)
        if terms.exists():
            return terms.first()
        else:
            return HttpResponse("No term matched your query.")

    def get_term_remark(term_avg):
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
        return term_remark

    def get_total_coefs(self, student):
        total_coef = student.get_sum_of_subjects_coef
        return total_coef

    def calculate_student_session_avg(self, student, session1_total):
        sum_of_coef = self.get_total_coefs(student)
        session_avg = session1_total / sum_of_coef

        return round(session_avg, 2)

    def get_term_avg(self, student, mxc_total):
        sum_of_coef = self.get_total_coefs(student)
        term_avg = mxc_total / sum_of_coef
        return round(term_avg, 2)

    def generate_student_report_data(self, student_id):
        # get all subjects for the current student
        student = self.get_student(student_id)

        subjects = self.get_all_subjects_for_a_given_student(student)

        term = self.get_term(self.__term_id)

        # get the sessions for the current term
        session1, session2 = ExaminationSession.objects.filter(term=term)

        sum_of_coef = self.get_total_coefs(student)

        # Go through all the subjects
        session_1_total_marks = 0
        session_2_total_marks = 0
        mxc_total = 0

        for subject in subjects:
            # check if subject has marks

            subject_mark_session1 = Mark.objects.filter(
                subject=subject, exam_session=session1, student=student
            )

            if not subject_mark_session1.exists():
                score1 = "/"
            else:
                teacher = subject_mark_session1.first().teacher.user.first_name
                score1 = subject_mark_session1.first().score

            subject_mark_session2 = Mark.objects.filter(
                subject=subject, exam_session=session2, student=student
            )

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

            self.data.append(
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
        session_1_avg = self.calculate_student_session_avg(
            student, session_1_total_marks
        )
        session_2_avg = self.calculate_student_session_avg(
            student, session_2_total_marks
        )
        term_avg = self.get_term_avg(student, mxc_total)

        term_remark = self.get_term_remark(term_avg)

        self.student_data = {
            "data": self.data,
            "name": student.user.get_fullname,
            "sum_of_coefs": sum_of_coef,
            "sequence1_total": session_1_total_marks,
            "sequence2_total": session_2_total_marks,
            "avg_sum": avg_sum,
            "mxc_sum": mxc_total,
            # avg data
            "session1_avg": session_1_avg,
            "session2_avg": session_2_avg,
            "term_avg": term_avg,
            "term_remark": term_remark,
        }
        return self.student_data

    def create_student_academic_records(self, student_id, klass):
        """
        Create and save a student academic record after all the marks have been calculated.
        """
        student = self.get_student(student_id)
        academic_record = AcademicRecord.objects.create(
            student=student,
            exam_term=self.get_term(self.__term_id),
            total_marks_obtained=self.data["mxc_sum"],
            student_rank=self.rank,
            term_avg=self.data["term_avg"],
            klass=klass,
            session_1_avg=self.data["session1_avg"],
            session_2_avg=self.data["session1_avg"],
        )
        try:
            academic_record.save()
            return True
        except Exception as e:
            return f"Error saving student records due to the following error \n {e}"


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

        if not subject_mark_session1.exists():
            score1 = "/"
        else:
            teacher = subject_mark_session1.first().teacher.user.first_name
            score1 = subject_mark_session1.first().score

        subject_mark_session2 = Mark.objects.filter(
            subject=subject, exam_session=session2, student=student
        )

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
        "name": student.user.get_fullname,
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
