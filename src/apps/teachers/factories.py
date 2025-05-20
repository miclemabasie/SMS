import factory
from datetime import datetime, time
from django.utils import timezone
from factory import Faker, fuzzy, SubFactory, post_generation
from faker import Faker as FakerFaker
from .models import TeacherProfile, User
from apps.users.factories import UserFactory
from factory.django import DjangoModelFactory
from apps.students.models import Class, Department

fake = FakerFaker()


class TeacherProfileFactory(DjangoModelFactory):
    class Meta:
        model = TeacherProfile

    user = factory.SubFactory(UserFactory)
    gender = fuzzy.FuzzyChoice(["M", "F", "Other"])
    phone_number = Faker("phone_number")
    main_subject = fuzzy.FuzzyChoice(
        ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History"]
    )
    address = Faker("street_address")

    # Regional information
    region_of_origin = Faker("text", max_chars=50)
    division_of_origin = Faker("text", max_chars=50)
    sub_division_of_origin = Faker("text", max_chars=50)
    country = Faker("country_code")
    town = Faker("city")
    location = Faker("city")

    # Career information
    date_recruitement_public_service = Faker("date_this_decade")
    corps = Faker("text", max_chars=50)
    service = Faker("sentence", nb_words=3)
    appointed_structure = Faker("company")
    possition_rank = Faker("job")

    # Grade and category information
    career_grade = fuzzy.FuzzyInteger(1, 10)
    payroll_grade = fuzzy.FuzzyInteger(1, 10)
    career_category = Faker("word")
    payroll_category_solde = Faker("word")

    # Index and echelon
    career_index = fuzzy.FuzzyInteger(1, 100)
    payroll_index = fuzzy.FuzzyInteger(1, 100)
    career_echelon = fuzzy.FuzzyInteger(1, 5)
    payroll_echelon = fuzzy.FuzzyInteger(1, 5)

    # Longevity information
    longivity_of_post = fuzzy.FuzzyInteger(1, 20)
    longivity_in_administration = fuzzy.FuzzyInteger(1, 30)

    # Administrative details
    appointment_decision_reference = Faker("isbn13")
    indemnity_situation = Faker("sentence", nb_words=5)

    # Optional fields
    profile_photo = factory.django.FileField(filename="profile.jpg")
    remark = Faker("sentence", nb_words=5)


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = Faker("word")
    code = Faker("bothify", text="DEPT-####")
    description = Faker("sentence")


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = Class

    grade_level = fuzzy.FuzzyChoice(["Form 1", "Form 2", "Form 3", "Form 4", "Form 5"])
    class_name = fuzzy.FuzzyChoice(["Science", "Arts", "Commercial", "General"])
    class_code = factory.Sequence(lambda n: f"CLS-{n:04d}")
    pass_avg = fuzzy.FuzzyInteger(50, 100)  # Promotion average

    # Relationships
    department = SubFactory(DepartmentFactory)

    # Optional fields with realistic defaults
    class_master = factory.SubFactory(
        UserFactory,
        is_teacher=True,
        teacher_profile__main_subject=fuzzy.FuzzyChoice(
            ["Mathematics", "English", "Science"]
        ),
    )

    class_prefect = factory.SubFactory(
        UserFactory,
        is_student=True,
        student_profile__current_class=factory.SelfAttribute(".."),
    )

    @factory.post_generation
    def handle_promotion_avg(self, create, extracted, **kwargs):
        if extracted is not None:
            self.pass_avg = extracted
            self.save()

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        # Ensure department exists if provided
        if "department" in kwargs and isinstance(kwargs["department"], int):
            kwargs["department"] = Department.objects.get(pkid=kwargs["department"])
        return super()._adjust_kwargs(**kwargs)
