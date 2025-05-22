# apps/academics/factories.py
import factory
from factory import Faker, fuzzy, SubFactory, LazyAttribute, post_generation
from factory.django import DjangoModelFactory
from decimal import Decimal
from apps.terms.factories import TermFactory
from apps.terms.models import Term
from .models import AcademicRecord


class AcademicRecordFactory(DjangoModelFactory):
    class Meta:
        model = AcademicRecord

    student = SubFactory("apps.users.factories.StudentProfileFactory")
    exam_term = factory.LazyFunction(
        lambda: Term.objects.filter(is_current=True).first()
        or TermFactory(is_current=True)
    )

    # Generate realistic academic performance data
    total_marks_obtained = fuzzy.FuzzyDecimal(200.0, 500.0, precision=2)
    term_avg = LazyAttribute(
        lambda o: (o.total_marks_obtained / Decimal("25.0")).quantize(Decimal(".01"))
    )

    # Session averages relative to term average
    session_1_avg = LazyAttribute(
        lambda o: max(
            Decimal("0.0"),
            o.term_avg * Decimal("0.85") + Decimal(fuzzy.random.uniform(-2, 2)),
        )
    )
    session_2_avg = LazyAttribute(
        lambda o: min(
            Decimal("20.0"),
            o.term_avg * Decimal("1.15") + Decimal(fuzzy.random.uniform(-2, 2)),
        )
    )

    # Class relationship handling
    klass = LazyAttribute(lambda o: o.student.current_class)

    # Generate realistic ranking
    student_rank = fuzzy.FuzzyInteger(1, 40)


class ReportCardFactory(DjangoModelFactory):
    class Meta:
        model = ReportCard

    student = SubFactory("apps.users.factories.StudentProfileFactory")
    session = factory.LazyAttribute(lambda o: o.academic_record.exam_term)
    generated_by = SubFactory("apps.users.factories.AdminProfileFactory")

    # Link to academic record
    @factory.post_generation
    def link_academic_record(self, create, extracted, **kwargs):
        if not create:
            return

        AcademicRecordFactory(
            student=self.student,
            exam_term=self.session,
            klass=self.student.current_class,
        )

    # Generate realistic remarks
    remark = fuzzy.FuzzyChoice(
        [
            "Consistent performance throughout the term",
            "Shows great improvement in practical subjects",
            "Needs to focus on core theoretical subjects",
            "Excellent participation in extracurricular activities",
            None,  # 20% chance of no remark
        ],
        weights=[3, 2, 2, 1, 2],
    )

    @classmethod
    def create_batch_for_class(cls, class_obj, size=30, **kwargs):
        """Create report cards for an entire class"""
        students = StudentProfileFactory.create_batch(size, current_class=class_obj)
        return [cls(student=student) for student in students]
