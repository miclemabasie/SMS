from typing import Any
from django.core.management.base import BaseCommand, CommandParser
import os


class Command(BaseCommand):
    help = "Renames a django project"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "new_project_name", type=str, help="The new django project name"
        )
        # parser.add_argument("-p", "--prefix")

        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        new_project_name = options["new_project_name"]

        # rename the django project
        files_to_rename = ["demo/settings/base.py", "demo/wsgi.py", "manage.py"]
        folder_to_rename = "demo"

        for f in files_to_rename:
            with open(f, "r") as file:
                filedata = file.read()

            filedata = filedata.replace("demo", new_project_name)

            with open(f, "w") as file:
                file.write(filedata)

        os.rename(folder_to_rename, new_project_name)

        self.stdout.write(
            self.style.SUCCESS(f"Project has been renamed to {new_project_name}.")
        )
        # return super().handle(*args, **options)
