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
        self.create_fake_users()
        self.create_parent()
        self.create_class()
        self.create_students()
        self.create_teachers()
        self.create_subjects()
        self.create_admin_staff()
        self.create_attendance()
        self.create_academic_year()
        self.create_term()
        self.create_exam_session()
        
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
            print(parent)

    def create_fake_users(self):
        "Creating fake users"
        for _ in range(50):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = faker.email()
            is_staff = False
            date_joined = timezone.now()
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
        for i in range(1, 31):
            student = StudentProfile.objects.create(
                user=User.objects.get(pkid=i),
                parent = ParentProfile.objects.get(pkid=i),
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
                user=User.objects.get(pkid=i),
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
                description=faker.text()
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
            att.save()

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
                term = random.choice(terms),
                academic_year = AcademicYear.objects.get(pkid=1)
            )
            term.save()


    def create_exam_session(self):
        seqs = ("first_seqence", "second_sequence", "third_sequence", "fourth_sequence", "fifth_sequence", "sixth_sequence")
        k = 1
        for i in range(0, 6):
            if i > 2:
                k = 2
            if i > 4:
                k = 3
            sess = ExaminationSession.objects.create(
                term = Term.objects.get(pkid=k),
                exam_session=seqs[i],
            )
            sess.save()
