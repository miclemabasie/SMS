import factory
from datetime import datetime, time
from django.utils import timezone
from factory import Faker, fuzzy, SubFactory, post_generation
from faker import Faker as FakerFaker
from apps.students.models import TeacherProfile, TEACHERSERVICE
from apps.users.factories import UserFactory
from apps.students.models import Subject
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model


User = get_user_model()

fake = FakerFaker()


class TeacherProfileFactory(DjangoModelFactory):
    class Meta:
        model = TeacherProfile

    user = factory.SubFactory(UserFactory)
    gender = fuzzy.FuzzyChoice(["M", "F", "Other"])
    phone_number = Faker("phone_number")
    main_subject = Subject.objects.order_by("?").first()
    address = Faker("street_address")

    # Regional information
    region_of_origin = Faker("text")
    division_of_origin = Faker("text")
    sub_division_of_origin = Faker("text")
    country = Faker("country_code")
    town = Faker("city")
    location = Faker("city")

    # Career information
    date_recruitement_public_service = Faker("date_this_decade")
    corps = Faker("text")
    service = fuzzy.FuzzyChoice(TEACHERSERVICE.values)
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
