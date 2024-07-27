import os
import random
from datetime import date
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from faker import Faker
from termcolor import colored

from apps.profiles.models import ParentProfile
from apps.staff.models import AdminProfile
from apps.students.models import (Attendance, Class, Mark, StudentProfile,
                                  Subject, TeacherProfile)
from apps.terms.models import AcademicYear, ExaminationSession, Term

User = get_user_model()

faker = Faker()

    # user = models.OneToOneField(User, related_name="student_profile", on_delete=models.CASCADE)
    

class Command(BaseCommand):
    help = "Auto Generate data for all the models in the system."


    def success_message(self, message):
        self.stdout.write(colored(message, "green"))

    def warning_message(self, message):
        self.stderr.write(colored(message, "yellow"))

    def handle(self, *args: Any, **options: Any) -> str | None:
        # new_project_name = options["new_project_name"]
        self.warning_message("=======================Starting to generate data =========================")
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
        self.warning_message("=======================Done with generating data.=========================")

        
        # return super().handle(*args, **options)

    def create_parent(self):
        roles = ["Father", "Mother", "Uncle", "Auntie"]
        for _ in range(30):
            parent = ParentProfile.objects.create(
                first_name = faker.user_name(),
                address = faker.address(),
                email = faker.email(),
                role = random.choice(roles)
                )
            parent.save()
            print(parent)

    def create_fake_users(self):
        "Creating fake users"
        self.warning_message("Creating Users...")
        for _ in range(50):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = faker.email()
            is_staff = False
            date_joined = timezone.now()
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, date_joined=date_joined)
            user.save()
        self.success_message("Users created.")

    def create_class(self):
        self.warning_message("Creating Classes...")
        for i in range(7):
            klass = Class.objects.create(
                class_name = faker.name(),
                grade_level = f"Form {str(i+1)}",
                class_master=faker.user_name(),
                class_prefect=faker.user_name()
            )
            klass.save()
        self.success_message("Classes Created.")
    
    def create_students(self):
        """Create fake data for student models"""
        self.warning_message("Creating Students.")
        for i in range(1, 31):
            user=User.objects.get(pkid=i)
            student = StudentProfile.objects.create(
                user = user,
                parent = ParentProfile.objects.get(pkid=i),
                current_class = Class.objects.get(pkid=random.randint(1, 6)),
                remark = faker.name(),
                gender = random.choice(["Male", "Female"]),
                address = faker.address(),
            )
            user.is_student = True
            user.save()
            student.save()
        self.success_message("Students have been created.")

    def create_teachers(self):
        """Create fake data for student models"""
        self.warning_message("Creating teachers.")
        for i in range(31, 46):
            user=User.objects.get(pkid=i)
            teacher = TeacherProfile.objects.create(
                user=user,
                location = faker.location_on_land()[2],
                remark = faker.name(),
                gender = random.choice(["Male", "Female"]),
                address = faker.address(),
            )
            user.is_teacher=True
            user.save()
            teacher.save()
        self.success_message("Teachers, Created.")

    def create_subjects(self):
        self.warning_message("Creating Subjects.")
        for _ in range(30):
            sub = Subject.objects.create(
                klass = Class.objects.get(pkid=random.randint(1, 7)),
                name=faker.cryptocurrency_name(),
                description=faker.text()
            )
            sub.save()
        self.success_message("Subjects Created.")

    def create_attendance(self):
        """Create attendance data"""
        self.warning_message("Creating attendance data.")
        for i in range(30):
            att = Attendance.objects.create(
                is_present = random.choice([False, True]),
                student = StudentProfile.objects.get(pkid=random.randint(1, 29)),
                teacher = TeacherProfile.objects.get(pkid=random.randint(1, 10)),
                subject = Subject.objects.get(pkid=random.randint(1, 20)),
            )
            att.save()
        self.success_message("Attendance data created.")

    def create_admin_staff(self):
        self.warning_message("Creating Administrator Data")
        for i in range(47, 51):
            user = User.objects.get(pkid=i)
            admin = AdminProfile.objects.create(
                user=user,
                location = faker.location_on_land()[2],
                address = faker.address(),
                can_manage = faker.text()
            )
            user.is_admin = True
            user.save()
            admin.save()
        self.success_message("Administor's data created.")

    def create_academic_year(self):
        self.warning_message("Creating Academic Year.")
        academic_year_2024_2025 = AcademicYear.objects.create(
            name="2024-2025",
            start_date=date(2024, 9, 1),  # Set the appropriate start date
            end_date=date(2025, 8, 31),   # Set the appropriate end date
        )
        academic_year_2024_2025.save()
        self.success_message("Done creating academic year")

    def create_term(self):
        self.warning_message("Creating Terms.")
        terms = ["first_term", "second_term", "third_term"]
        for i in range(1, 4):
            term = Term.objects.create(
                term = terms[i-1],
                academic_year = AcademicYear.objects.get(pkid=1)
            )
            term.save()
        self.success_message("Done creating term data.")


    def create_exam_session(self):
        self.warning_message("Creating examination sessions.")
        seqs = ("first_sequence", "second_sequence", "third_sequence", "fourth_sequence", "fifth_sequence", "sixth_sequence")
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
        self.success_message("Examination sessions created.")
