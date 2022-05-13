from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

USERNAME = "admin"
PASSWORD = "admin"
EMAIL = "admin@example.com"


class Command(BaseCommand):
    """
    Create a superuser with the given username, password and email from commandline
    or using the default values
    Example:
        manage.py create_admin --username=admin --password=admin --email=admin@admin.com
        or
        manage.py create_admin
    """

    def add_arguments(self, parser):
        parser.add_argument("--username", default=USERNAME, required=False)
        parser.add_argument("--password", default=PASSWORD, required=False)
        parser.add_argument("--email", default=EMAIL, required=False)

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        email = options["email"]

        user_model = get_user_model()

        try:
            user_model.objects.create_superuser(
                username=username, password=password, email=email
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser: {username} was created"))

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(f"Superuser: {username} already exists")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Superuser: {username} couldn't be created. {str(e)}")
            )
