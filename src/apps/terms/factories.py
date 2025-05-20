from factory import Faker, fuzzy, post_generation, SubFactory
from faker import Faker as FakerFaker
from .models import AcademicYear, Term, ExaminationSession
from factory.django import DjangoModelFactory

fake = FakerFaker()


class AcademicYearFactory(DjangoModelFactory):
    class Meta:
        model = AcademicYear

    name = Faker("year")

    # @post_generation  # type: ignore
    # def terms(self, create, extracted, **kwargs):
    #     """
    #     Create terms for the academic year
    #     """
    #     if not create:  # this checks if the object is being created
    #         return

    #     if extracted:
    #         for term in extracted:
    #             self.terms.add(term)


class TermFactory(DjangoModelFactory):
    class Meta:
        model = Term

    term = Faker("word")
    academic_year = SubFactory(AcademicYearFactory)


class ExaminationSessionFactory(DjangoModelFactory):
    class Meta:
        model = ExaminationSession

    exam_session = Faker("word")
    term = SubFactory(TermFactory)
