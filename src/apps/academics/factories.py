import factory
from datetime import datetime, time
from django.utils import timezone
from factory import (
    Faker,
    fuzzy,
    SubFactory,
    SubFactory,
    Maybe,
    LazyAttribute,
    post_generation,
)
from faker import Faker as FakerFaker
from apps.users.factories import UserFactory
from factory.django import DjangoModelFactory
from apps.students.models import Class, Department, Subject


fake = FakerFaker()


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = Faker("word")


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = Class

    grade_level = fuzzy.FuzzyChoice(["Form 1", "Form 2", "Form 3", "Form 4", "Form 5"])
    class_name = fuzzy.FuzzyChoice(["Science", "Arts", "Commercial", "General"])
    class_code = factory.Sequence(lambda n: f"CLS-{n:04d}")
    pass_avg = fuzzy.FuzzyInteger(8, 12)  # Promotion average

    # Relationships
    department = SubFactory(DepartmentFactory)

    # # Optional fields with realistic defaults
    # class_master = factory.SubFactory(
    #     UserFactory,
    #     is_teacher=True,
    #     teacher_profile__main_subject=fuzzy.FuzzyChoice(
    #         ["Mathematics", "English", "Science"]
    #     ),
    # )

    # class_prefect = factory.SubFactory(
    #     UserFactory,
    #     is_student=True,
    #     student_profile__current_class=factory.SelfAttribute(".."),
    # )


# apps/academics/factories.py


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name = Faker(
        "word",
        ext_word_list=[
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "English",
            "History",
            "Geography",
            "Computer Science",
        ],
    )

    code = factory.Sequence(lambda n: f"SUBJ-{n:03d}")
    description = Faker("paragraph", nb_sentences=3)
    coef = fuzzy.FuzzyInteger(1, 5)  # More realistic coefficient range

    # Conditional class relationship (70% chance of having a class)
    klass = Maybe(
        fuzzy.FuzzyChoice([True, False]),
        yes_declaration=SubFactory("apps.academics.factories.ClassFactory"),
        no_declaration=None,
    )

    # # Conditional teacher assignment (50% chance)
    assigned_to = Maybe(
        fuzzy.FuzzyChoice([True, False]),
        yes_declaration=SubFactory("apps.teachers.factories.TeacherProfileFactory"),
        no_declaration=None,
    )

    # Automatically set boolean flags based on relationships
    has_class = LazyAttribute(lambda o: o.klass is not None)
    assigned = LazyAttribute(lambda o: o.assigned_to is not None)

    @factory.post_generation
    def add_to_class(self, create, extracted, **kwargs):
        """Post-generation hook to handle class-subject relationships"""
        if create and self.klass:
            self.klass.subjects.add(self)
            self.klass.save()
