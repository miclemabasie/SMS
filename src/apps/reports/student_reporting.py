from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponse

from apps.students.models import Class, ClassAcademicRecord, Mark, Subject
from apps.terms.models import AcademicYear, ExaminationSession, Term

from .models import AcademicRecord, StudentProfile


class ClassPerformanceReport:

    def __init__(self, class_id, term_id):
        self.__class_id = class_id
        self.__term_id = term_id
        self.data = []
        self.sub_dicts = self.get_all_subjects_for_class()

    def setup(self):
        # this function is called first to make sure generation of data is possible
        try:
            term = self.get_term()
        except:
            return "Can not get term data"

        # get the sessions for the current term
        try:
            session1, session2 = ExaminationSession.objects.filter(term=term)
        except:
            return "Can not get session data"
        return None

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

    def get_all_subjects_for_a_given_student(self, student):
        subjects = student.get_all_subjects()
        return subjects

    def get_all_subjects_for_class(self):
        class_ = self.get_class()
        subjects = class_.subjects.all()
        subjects_dict = {sub.name: 0 for sub in subjects}
        return subjects_dict

    def get_term(self):
        # get the term
        terms = Term.objects.filter(pkid=self.__term_id)
        if terms.exists():
            return terms.first()
        else:
            return HttpResponse("No term matched your query.")

    def get_first_term_report_data(self, student):
        # get the student report data for the first term
        academic_record = AcademicRecord.objects.filter(
            exam_term__term__icontains="First Term", student=student
        )
        if academic_record.exists():
            academic_record = academic_record.first()
            return academic_record.term_avg
        else:
            return -1

    def get_second_term_report_date(self, student):
        academic_record = AcademicRecord.objects.filter(
            exam_term__term__icontains="Second Term", student=student
        )
        if academic_record.exists():
            academic_record = academic_record.first()
            return academic_record.term_avg
        else:
            return -1

    def is_first_term(self):
        term = self.get_term()
        if term.term == "First Term":
            return True
        else:
            return False

    def is_second_term(self):
        term = self.get_term()
        if term.term == "Second Term":
            return True
        else:
            return False

    def is_third_term(self):
        term = self.get_term()
        if term.term == "Third Term":
            return True
        else:
            return False

    def get_promotion_decision(self, student, annual_avg):
        klass = self.get_class()
        if annual_avg < klass.pass_avg:
            student.is_repeater = True
            student.save()
            return "Repeat"
        elif annual_avg > klass.pass_avg:
            student.is_repeater = False
            student.save()
            return "Promoted"

    def get_annual_avg(self, third_term_avg, student):
        if self.is_third_term():
            first_term_avg = self.get_first_term_report_data(student)
            second_term_avg = self.get_second_term_report_date(student)
            annual_avg = (
                Decimal(first_term_avg)
                + Decimal(second_term_avg)
                + Decimal(third_term_avg)
            ) / Decimal(3)
            return round(annual_avg, 2)
        else:
            return -1

    def get_term_remark(self, term_avg) -> str:
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
        total_coef = student.get_sum_of_subjects_coef()
        return total_coef

    def calculate_student_session_avg(self, student, session1_total):
        sum_of_coef = self.get_total_coefs(student)
        session_avg = session1_total / sum_of_coef

        return round(session_avg, 2)

    def get_term_avg(self, student, mxc_total):
        sum_of_coef = self.get_total_coefs(student)
        term_avg = mxc_total / sum_of_coef
        return round(term_avg, 2)

    def generate_student_report_data(self, student):
        # get all subjects for the current student

        subjects = self.get_all_subjects_for_a_given_student(student)

        term = self.get_term()

        # get the sessions for the current term

        session1, session2 = ExaminationSession.objects.filter(term=term)

        sum_of_coef = self.get_total_coefs(student)

        # Go through all the subjects
        session_1_total_marks = 0
        session_2_total_marks = 0
        mxc_total = 0

        data = []
        for subject in subjects:
            # check if subject has marks
            subject_mark_session1 = Mark.objects.filter(
                subject=subject, exam_session=session1, student=student
            )

            if not subject_mark_session1.exists():
                score1 = "/"
            else:
                teacher = subject_mark_session1.first().get_teacher()
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

            self.update_subject_total_score(self.sub_dicts, subject.name, mxc)

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

        student_data = {
            "data": data,
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

        return student_data

    def update_subject_total_score(self, subject_dict, subject, mxc):
        if mxc != "/":
            subject_dict[subject] += mxc

    def create_student_academic_records(self, student, data, rank):
        """
        Create and save a student academic record after all the marks have been calculated.
        """
        academic_record = AcademicRecord.objects.filter(
            student=student, exam_term=self.get_term()
        )
        if academic_record.exists():
            academic_record = academic_record.first()
        else:
            academic_record, created = AcademicRecord.objects.get_or_create(
                student=student,
                exam_term=self.get_term(),
                total_marks_obtained=data["mxc_sum"],
                student_rank=rank,
                term_avg=data["term_avg"],
                klass=self.get_class(),
                session_1_avg=data["session1_avg"],
                session_2_avg=data["session1_avg"],
            )
        try:
            # update the academic record before saving
            academic_record.total_marks_obtained = (data["mxc_sum"],)
            academic_record.student_rank = (rank,)
            academic_record.term_avg = (data["term_avg"],)
            academic_record.klass = (self.get_class(),)
            academic_record.session_1_avg = (data["session1_avg"],)
            academic_record.session_2_avg = (data["session1_avg"],)
            academic_record.save()
            return True
        except Exception as e:
            return f"Error saving student records due to the following error \n {e}"

    def get_all_students_for_current_class(self):
        students = StudentProfile.objects.filter(current_class=self.get_class())
        return students

    def get_total_students_per_class(self):
        klass = self.get_class()
        students = StudentProfile.objects.filter(current_class=klass)
        return len(students)

    def get_class_avg(self):
        class_avg = (self.generate_performacne_rank_list()["total_avg"] * 20) / (
            self.get_total_students_per_class() * 20
        )
        return round(class_avg, 2)

    def generate_performacne_rank_list(self) -> list:
        # get all students for the current class
        total_avgs = 0
        students = self.get_all_students_for_current_class()
        class_performance = []
        for s in students:
            s_marks = self.generate_student_report_data(s)["term_avg"]
            total_avgs += s_marks
            class_performance.append((s, s_marks))

        class_performance = sorted(
            class_performance,
            key=lambda x: x[1],
            reverse=True,
        )

        data = {"class_performance": class_performance, "total_avg": total_avgs}

        return data

    def get_student_rank(self, student, class_performance):
        student_ranking = [
            rank + 1
            for rank, (s, _) in enumerate(class_performance)
            if s.pkid == student.pkid
        ][0]
        return student_ranking

    def generate_file_name(self):
        term = self.get_term()
        klass = self.get_class()
        return f"{klass.get_full_name()}-{term.term}"

    def find_largest_subject_score(self):
        highest_score = 0
        highest_subject = None
        print("we are print none because there is no subject ", self.sub_dicts.items())

        for subject, score in self.sub_dicts.items():
            if score > highest_score:
                highest_score = score
                highest_subject = subject
        if highest_subject is not None:
            data = {highest_subject: highest_score}
            print("data", data)
            return data

        return None

    def find_lowest_subject_score(self):
        if self.find_largest_subject_score() is not None:
            lowest_score = list(self.find_largest_subject_score().values())[0]
            lowest_subject = list(self.find_largest_subject_score().keys())[0]

            for subject, score in self.sub_dicts.items():
                if score < lowest_score:
                    lowest_score = score
                    lowest_subject = subject
            if lowest_subject is not None:
                data = {lowest_subject: score}
                return data

        return None

    def set_highest_subject_score_to_class(self):
        class_ = self.get_class()
        subject = self.find_largest_subject_score()
        subject_lowest = self.find_lowest_subject_score()
        if subject is not None:
            class_.best_subject = list(subject.keys())[0]
            class_.worst_subject = list(subject_lowest.keys())[0]
            class_.save()

    def get_single_report_name(self, student):
        term = self.get_term()
        class_ = self.get_class()
        name = f"{student.user.get_fullname} {term.term}-{class_.get_class_name}-progress-report"
        return name

    def create_class_report_data(self, klass, term, class_avg):
        print("trying to make report data.")
        report, created = ClassAcademicRecord.objects.get_or_create(
            klass=klass, term=term
        )
        report.class_avg = class_avg
        report.save()
        return report
        # if created:
        #     report.save()
        #     return report
        # else:
        #     # update the report
        #     report.class_avg = class_avg
        #     report.save()
        #     return report
