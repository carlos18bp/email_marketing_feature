from django.core.management.base import BaseCommand
from email_marketing_feature_app.models import User, Email, UserEmail

class Command(BaseCommand):
    help = 'Create rake records in the database'

    """
    To delete fake data via console, run:
    python3 manage.py delete_fake_data
    """
    def handle(self, *args, **options):
        User.objects.all().delete()
        Email.objects.all().delete()
        UserEmail.objects.all().delete()