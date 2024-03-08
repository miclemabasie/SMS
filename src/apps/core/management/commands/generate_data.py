from typing import Any
from django.core.management.base import BaseCommand, CommandParser
import os
from django.utils import timezone
from faker import Faker
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, Class, Attendance, Subject, Mark, TeacherProfile
from apps.staff.models import AdminProfile
from apps.profiles.models import ParentProfile
from apps.terms.models import AcademicYear, Term, ExaminationSession
from datetime import date


import random

User = get_user_model()

faker = Faker()

    # user = models.OneToOneField(User, related_name="student_profile", on_delete=models.CASCADE)
    

class Command(BaseCommand):
    help = "Renames a django project"

    # def add_arguments(self, parser: CommandParser) -> None:
    #     parser.add_argument(
    #         "new_project_name", type=str, help="The new django project name"
    #     )
    #     # parser.add_argument("-p", "--prefix")

    #     return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        # new_project_name = options["new_project_name"]
        self.create_students()
        
        # return super().handle(*args, **options)

    def create_parent(self):
        roles = ["Father", "Mother", "Uncle", "Auntie"]
        for _ in range(30):
            parent = ParentProfile.objects.create(
                full_name = faker.user_name(),
                address = faker.address(),
                email = faker.email(),
                role = random.choice(roles)
                )
            parent.save()

    def create_fake_users(self):
        for _ in range(50):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = faker.email()
            is_staff = False
            date_joined = timezone.now
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, date_joined=date_joined)
            user.save()

    def create_class(self):
        for i in range(7):
            klass = Class.objects.create(
                class_name = faker.name(),
                grade_level = f"Form {str(i+1)}"
            )
            klass.save()
    
    def create_students(self):
        """Create fake data for student models"""
        print("This is to crate data about student")
        for i in range(30):
            student = StudentProfile.objects.create(
                user=User.objects.get(i),
                parent = ParentProfile.object.get(pkid=i),
                current_class = Class.objects.get(pkid=random.randint(1, 6)),
                remark = faker.name(),
                gender = random.choice(["Male", "Female"]),
                address = faker.address(),
            )
            student.save()

    def create_teachers(self):
        """Create fake data for student models"""
        print("This is to crate data about student")
        for i in range(31, 46):
            teacher = TeacherProfile.objects.create(
                user=User.objects.get(i),
                location = faker.location_on_land()[2],
                remark = faker.name(),
                gender = random.choice(["Male", "Female"]),
                address = faker.address(),
            )
            teacher.save()

    def create_subjects(self):
        for _ in range(30):
            sub = Subject.objects.create(
                klass = Class.objects.get(pkid=random.randint(1, 7)),
                name=faker.cryptocurrency_name(),
                descrition=faker.text()
            )
            sub.save()


    def create_attendance(self):
        """Create attendance data"""
        for i in range(30):
            att = Attendance.objects.create(
                is_present = random.choice([False, True]),
                student = StudentProfile.objects.get(pkid=random.randint(1, 29)),
                teacher = TeacherProfile.objects.get(pkid=random.randint(1, 10)),
                subject = Subject.objects.get(pkid=random.randint(1, 20)),
            )
            att.save(0)

    def create_admin_staff(self):
        for i in range(47, 51):
            admin = AdminProfile.objects.create(
                user = User.objects.get(pkid=i),
                location = faker.location_on_land()[2],
                address = faker.address(),
                can_manage = faker.text()
            )
            admin.save()

    def create_academic_year(self):

        academic_year_2024_2025 = AcademicYear.objects.create(
            name="2024-2025",
            start_date=date(2024, 9, 1),  # Set the appropriate start date
            end_date=date(2025, 8, 31),   # Set the appropriate end date
        )
        academic_year_2024_2025.save()

    def create_term(self):
        terms = ["first_term", "second_term", "third_term"]
        for _ in range(1, 3):
            term = Term.objects.create(
                term = random.choice(terms)
            )
            term.save()


    def create_exam_session(self):
        seqs = ("first_seqence", "second_sequence", "third_sequence", "fourth_sequence", "fifth_sequence", "sixth_sequence")
        k = 1
        for i in range(1, 7):
            if i > 2:
                k = 2
            if i > 4:
                k = 3
            sess = ExaminationSession.objects.create(
                term = Term.objects.get(pkid=k)
                exam_session=seqs[i],
            )
            sess.save()

 


faker11 = ['__annotations__', '__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_factories', '_factory_map', '_locales', '_map_provider_method', '_optional_proxy', '_select_factory', '_select_factory_choice', '_select_factory_distribution', '_unique_proxy', '_weights', 'aba', 'add_provider', 'address', 'administrative_unit', 'am_pm', 'android_platform_token', 'ascii_company_email', 'ascii_email', 'ascii_free_email', 'ascii_safe_email', 'bank_country', 'basic_phone_number', 'bban', 'binary', 'boolean', 'bothify', 'bs', 'building_number', 'cache_pattern', 'catch_phrase', 'century', 'chrome', 'city', 'city_prefix', 'city_suffix', 'color', 'color_hsl', 'color_hsv', 'color_name', 'color_rgb', 'color_rgb_float', 'company', 'company_email', 'company_suffix', 'coordinate', 'country', 'country_calling_code', 'country_code', 'credit_card_expire', 'credit_card_full', 'credit_card_number', 'credit_card_provider', 'credit_card_security_code', 'cryptocurrency', 'cryptocurrency_code', 'cryptocurrency_name', 'csv', 'currency', 'currency_code', 'currency_name', 'currency_symbol', 'current_country', 'current_country_code', 'date', 'date_between', 'date_between_dates', 'date_object', 'date_of_birth', 'date_this_century', 'date_this_decade', 'date_this_month', 'date_this_year', 'date_time', 'date_time_ad', 'date_time_between', 'date_time_between_dates', 'date_time_this_century', 'date_time_this_decade', 'date_time_this_month', 'date_time_this_year', 'day_of_month', 'day_of_week', 'del_arguments', 'dga', 'domain_name', 'domain_word', 'dsv', 'ean', 'ean13', 'ean8', 'ein', 'email', 'emoji', 'enum', 'factories', 'file_extension', 'file_name', 'file_path', 'firefox', 'first_name', 'first_name_female', 'first_name_male', 'first_name_nonbinary', 'fixed_width', 'format', 'free_email', 'free_email_domain', 'future_date', 'future_datetime', 'generator_attrs', 'get_arguments', 'get_formatter', 'get_providers', 'hex_color', 'hexify', 'hostname', 'http_method', 'http_status_code', 'iana_id', 'iban', 'image', 'image_url', 'internet_explorer', 'invalid_ssn', 'ios_platform_token', 'ipv4', 'ipv4_network_class', 'ipv4_private', 'ipv4_public', 'ipv6', 'isbn10', 'isbn13', 'iso8601', 'items', 'itin', 'job', 'json', 'json_bytes', 'language_code', 'language_name', 'last_name', 'last_name_female', 'last_name_male', 'last_name_nonbinary', 'latitude', 'latlng', 'lexify', 'license_plate', 'linux_platform_token', 'linux_processor', 'local_latlng', 'locale', 'locales', 'localized_ean', 'localized_ean13', 'localized_ean8', 'location_on_land', 'longitude', 'mac_address', 'mac_platform_token', 'mac_processor', 'md5', 'military_apo', 'military_dpo', 'military_ship', 'military_state', 'mime_type', 'month', 'month_name', 'msisdn', 'name', 'name_female', 'name_male', 'name_nonbinary', 'nic_handle', 'nic_handles', 'null_boolean', 'numerify', 'opera', 'optional', 'paragraph', 'paragraphs', 'parse', 'passport_dates', 'passport_dob', 'passport_full', 'passport_gender', 'passport_number', 'passport_owner', 'password', 'past_date', 'past_datetime', 'phone_number', 'port_number', 'postalcode', 'postalcode_in_state', 'postalcode_plus4', 'postcode', 'postcode_in_state', 'prefix', 'prefix_female', 'prefix_male', 'prefix_nonbinary', 'pricetag', 'profile', 'provider', 'providers', 'psv', 'pybool', 'pydecimal', 'pydict', 'pyfloat', 'pyint', 'pyiterable', 'pylist', 'pyobject', 'pyset', 'pystr', 'pystr_format', 'pystruct', 'pytimezone', 'pytuple', 'random', 'random_choices', 'random_digit', 'random_digit_above_two', 'random_digit_not_null', 'random_digit_not_null_or_empty', 'random_digit_or_empty', 'random_element', 'random_elements', 'random_int', 'random_letter', 'random_letters', 'random_lowercase_letter', 'random_number', 'random_sample', 'random_uppercase_letter', 'randomize_nb_elements', 'rgb_color', 'rgb_css_color', 'ripe_id', 'safari', 'safe_color_name', 'safe_domain_name', 'safe_email', 'safe_hex_color', 'sbn9', 'secondary_address', 'seed', 'seed_instance', 'seed_locale', 'sentence', 'sentences', 'set_arguments', 'set_formatter', 'sha1', 'sha256', 'simple_profile', 'slug', 'ssn', 'state', 'state_abbr', 'street_address', 'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'suffix_nonbinary', 'swift', 'swift11', 'swift8', 'tar', 'text', 'texts', 'time', 'time_delta', 'time_object', 'time_series', 'timezone', 'tld', 'tsv', 'unique', 'unix_device', 'unix_partition', 'unix_time', 'upc_a', 'upc_e', 'uri', 'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid4', 'vin', 'weights', 'windows_platform_token', 'word', 'words', 'xml', 'year', 'zip', 'zipcode', 'zipcode_in_state', 'zipcode_plus4']