# apps/users/factories.py
import factory
from factory import Faker, fuzzy, SubFactory, post_generation
from factory.django import DjangoModelFactory
from django.utils import timezone
from .models import AdminProfile, Role, Gender


class AdminProfileFactory(DjangoModelFactory):
    class Meta:
        model = AdminProfile

    user = factory.SubFactory(
        "apps.users.factories.UserFactory", is_admin=True, is_staff=True
    )

    # Personal Information
    gender = fuzzy.FuzzyChoice(Gender.values)
    phone_number = Faker("phone_number")
    address = Faker("street_address")
    location = Faker("city")
    country = Faker("country_code")
    profile_photo = factory.django.ImageField(filename="admin.jpg")

    # Professional Information
    role = fuzzy.FuzzyChoice(Role.values)
    responsibilities = Faker("sentence", nb_words=6)
    number_of_absences = fuzzy.FuzzyInteger(0, 20)

    # Permissions
    can_manage = fuzzy.FuzzyChoice(["All", "Students", "Teachers", "Academic"])
    generate_reports = fuzzy.FuzzyChoice([True, False])
    manage_students = fuzzy.FuzzyChoice([True, False])
    manage_teachers = fuzzy.FuzzyChoice([True, False])
    manage_admins = fuzzy.FuzzyChoice([True, False])
    manage_sessions = fuzzy.FuzzyChoice([True, False])
    manage_subjects = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def remark(self):
        return f"Admin remark for {self.user.username}"

    # Automatic fields handling
    @factory.post_generation
    def set_permissions_based_on_role(self, create, extracted, **kwargs):
        if not create:
            return

        # Role-based permission logic
        if self.role == Role.PRINCIPAL:
            self.manage_teachers = True
            self.manage_students = True
            self.generate_reports = True
        elif self.role == Role.IT:
            self.manage_sessions = True
            self.manage_subjects = True
