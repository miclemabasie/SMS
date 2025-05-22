# apps/students/factories.py
import factory
from datetime import datetime, time
from django.utils import timezone
from factory import Faker, fuzzy, SubFactory, LazyAttribute, post_generation
from faker import Faker as FakerFaker
from apps.users.factories import UserFactory
from apps.academics.factories import ClassFactory
from .models import StudentProfile, ParentProfile
from django.contrib.auth import get_user_model
from .utils import (
    create_student_pin,
)


User = get_user_model()

fake = FakerFaker()


def generate_student_dob():
    date = fake.date_of_birth(minimum_age=10, maximum_age=18)
    return timezone.make_aware(datetime.combine(date, time(8, 51, 2)))


class ParentProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParentProfile

    first_name = Faker("first_name")
    occupation = Faker("job")
    phone = Faker("phone_number")
    email = Faker("email")
    address = Faker("street_address")
    role = fuzzy.FuzzyChoice(["Father", "Mother", "Guardian", "Other"])


class StudentUserFactory(UserFactory):
    class Meta:
        model = User  # Ensure this points to your custom User model

    is_student = True
    dob = factory.LazyFunction(generate_student_dob)

    # Override username generation to prevent conflicts
    username = factory.LazyAttributeSequence(lambda o, n: f"{o.first_name.lower()}{n}")


class StudentProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentProfile

    user = factory.SubFactory(StudentUserFactory)
    parent = factory.SubFactory(ParentProfileFactory)
    current_class = factory.SubFactory(ClassFactory)

    # Required fields
    gender = fuzzy.FuzzyChoice(["M", "F", "Other"])
    phone_number = Faker("phone_number")
    address = Faker("street_address")
    domain = fuzzy.FuzzyChoice(["Science", "Arts", "Commercial", "General"])

    # Optional fields
    profile_photo = factory.django.FileField(filename="student.jpg")

    # PIN handling
    @factory.post_generation
    def create_pin(self, create, extracted, **kwargs):
        if create:
            pin = fake.numerify(text="####")
            create_student_pin(self, pin)

    # # Handle view-specific logic
    # @classmethod
    # def _after_postgeneration(cls, instance, create, results=None):
    #     super()._after_postgeneration(instance, create, results)
    #     if create:
    #         send_account_creation_email(None, instance.user)
