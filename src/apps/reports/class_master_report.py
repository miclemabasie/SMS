from apps.students.models import StudentProfile, Class, Mark
from .models import AcademicRecord
from apps.terms.models import Term


class ClassMasterReport:

    def __init__(self, class_id, term_id) -> None:
        self.__class_id = class_id
        self.__term_id = term_id

        print("Initializing class master report")

    def get_class(self):
        classes = Class.objects.filter(pkid=self.__class_id)
        if classes.exists():
            class_ = classes.first()
            return class_
        return None

    def get_term(self):
        terms = Term.objects.filter(pkid=self.__term_id)
        if terms.exists():
            term = terms.first()
            return term
        return None

    def generate_class_mater_report(self):
        best_students = self.get_best_students_from_class()
        last_studenst = self.get_worst_students_from_class()
        total_boys = self.get_total_males_from_class()
        total_girls = self.get_total_girls_from_class()

    def get_best_students_from_class(self):
        students = AcademicRecord.get_best_three_students()
        return students

    def get_worst_students_from_class(self):
        students = AcademicRecord.get_last_three_students()
        return students

    def get_total_males_from_class(self):
        class_ = self.get_class()
        total = class_.get_total_boys()
        return total

    def get_total_girls_from_class(self):
        class_ = self.get_class()
        total = class_.get_total_girls()
        return total

    def get_all_passed(self):
        class_ = self.get_class()
        term = self.get_term()
        all_passed = AcademicRecord.get_number_passed_in_a_term(
            term, class_, class_.pass_avg
        )
        return all_passed

    # def get_total_failed(self):
    #     class_ = self.get_class()
    #     term = self.get_term()
    #     total_failed = AcademicRecord.get_number_failed_in_a_term(
    #         term, class_, class_.pass_avg
    #     )
    #     return total_failed

    def get_total_girls_passed(self):
        all_passed = self.get_all_passed()  # returns a queryset
        females_passed = all_passed.filter(student__gender="Female")
        return len(females_passed)

    def get_total_boys_passed(self):
        all_passed = self.get_all_passed()  # returns a queryset
        males_passed = all_passed.filter(student__gender="Male")
        return len(males_passed)

    def get_total_passed(self):
        return len(self.get_all_passed())

    def get_highest_student(self):
        class_ = self.get_class()
        term = self.get_term()
        highest_student = AcademicRecord.get_highest_student_in_a_term(
            term, class_, class_.pass_avg
        )
        return highest_student

    def get_highest_student_avg(self):
        return self.get_highest_student().term_avg

    def get_last_student(self):
        class_ = self.get_class()
        term = self.get_term()
        lowest_student = AcademicRecord.get_lowest_student_in_a_term(
            term, class_, class_.pass_avg
        )
        return lowest_student

    def get_lowest_student_avg(self):
        return self.get_last_student().term_avg
