from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Renames a Django project"

    def add_arguments(self, parser):
        parser.add_argument("new_project_name", type=str,
                            help="The new django project name")

    def handle(self, *args, **kwargs):
        new_project_name = kwargs["new_project_name"]

        # logic

        files_to_rename = ["demo/settings/base.py",
                           "demo/wsgi.py", "manage.py"]
        folder_to_rename = "demo"

        for files in files_to_rename:
            with open(files, "r") as f:
                filedata = f.read()

            filedata = filedata.replace("demo", new_project_name)

            with open(files, "w") as f:
                f.write(filedata)

        os.rename(folder_to_rename, new_project_name)

        self.stdout.write(self.style.SUCCESS(
            f"PROJECT HAS BEEN SUCCESSFULLY RENAMED FROM DEMO TO {new_project_name}"))
