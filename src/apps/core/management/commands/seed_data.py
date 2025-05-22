from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

# Import your factories
from apps.users.factories import UserFactory
from apps.students.factories import StudentProfileFactory
from apps.teachers.factories import TeacherProfileFactory
from apps.academics.factories import ClassFactory, DepartmentFactory, SubjectFactory
from apps.settings.factories import SettingFactory
from apps.staff.factories import AdminProfileFactory


class Command(BaseCommand):

    # make sure the accademic year and term are created
    help = "Seed database with factory-generated data in batches"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=10,
            help="Number of records to create per model",
        )
        parser.add_argument(
            "--models",
            type=str,
            help="Comma-separated list of models to seed (users,teachers,students,classes,settings)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        valid_models = {
            "admins": AdminProfileFactory,
            "teachers": TeacherProfileFactory,
            "students": StudentProfileFactory,
            "departments": DepartmentFactory,
            "classes": ClassFactory,
            "subjects": SubjectFactory,
        }

        # selected_models = (
        #     options["models"].split(",") if options["models"] else valid_models.keys()
        # )
        selected_models = valid_models.keys()
        batch_size = options["batch_size"]

        created_counts = {}

        for model_name in selected_models:
            if model_name not in valid_models:
                self.stderr.write(
                    self.style.ERROR(
                        f"Invalid model '{model_name}'. Valid options: {', '.join(valid_models.keys())}"
                    )
                )
                continue

            factory = valid_models[model_name]
            self.stdout.write(
                self.style.SQL_KEYWORD(f"→ Creating {batch_size} {model_name}...")
            )
            if model_name == "admins":
                batch_size = 5
            elif model_name == "departments":
                batch_size = 3
            elif model_name == "classes":
                batch_size = 10
            elif model_name == "subjects":
                batch_size = 20
            elif model_name == "teachers":
                batch_size = 10
            elif model_name == "students":
                batch_size = 100

            created_counts[model_name] = factory.create_batch(batch_size)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Created {len(created_counts[model_name])} {model_name}"
                )
            )

        # Print summary
        self.stdout.write("\n" + self.style.SUCCESS("Seeding complete!"))
        for model, count in created_counts.items():
            self.stdout.write(f"• {model.capitalize()}: {len(count)} created")
