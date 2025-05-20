import factory
from datetime import datetime, time
from django.utils import timezone
from factory import Faker, fuzzy, post_generation
from faker import Faker as FakerFaker
from .models import TeacherProfile, User

fake = FakerFaker()


def generate_dob():
    date = fake.date_of_birth(minimum_age=21, maximum_age=65)
    return timezone.make_aware(datetime.combine(date, time(8, 51, 2)))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    is_teacher = True
    dob = factory.LazyFunction(generate_dob)

    @post_generation
    def set_password(self, create, extracted, **kwargs):
        if create:
            password = fake.password()
            self.set_password(password)
            self.save()
