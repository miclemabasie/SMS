import factory
from decimal import Decimal
from django.utils import timezone
from factory import Faker, fuzzy
from .models import Setting


class SettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Setting

    # File fields with dummy files
    school_logo = factory.django.FileField(filename="logo.png")
    school_favicon = factory.django.FileField(filename="favicon.ico")

    # Text fields with realistic data
    school_name = Faker("company")
    currency = fuzzy.FuzzyChoice(["CFA", "XAF"])
    city = Faker("city")
    postal_code = Faker("postcode")
    address1 = Faker("street_address")
    address2 = Faker("secondary_address")
    country = "CM"  # Default country code for Cameroon
    motto = Faker("sentence", nb_words=6)

    # Numerical fields with model defaults
    highest_upload_mark = 20
    first_installment = Decimal("10000.00")
    second_installment = Decimal("10000.00")
    pta = Decimal("10000.00")
    school_uniform = Decimal("10000.00")

    # Date field with current timestamp
    next_opening_date = factory.LazyFunction(timezone.now)

    # Boolean field with default
    teacher_can_upload = False
