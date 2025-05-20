from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

# Import your factories
from apps.users.factories import UserFactory
from apps.students.factories import StudentProfileFactory
from apps.teachers.factories import TeacherProfileFactory
from apps.teachers.factories import ClassFactory, DepartmentFactory
from apps.settings.factories import SettingFactory


class Command(BaseCommand):
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
            "users": UserFactory,
            "teachers": TeacherProfileFactory,
            "students": StudentProfileFactory,
            "departments": DepartmentFactory,
            "classes": ClassFactory,
            "settings": SettingFactory,
        }

        selected_models = (
            options["models"].split(",") if options["models"] else valid_models.keys()
        )
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
