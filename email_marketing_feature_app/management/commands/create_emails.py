from django.core.management.base import BaseCommand
from faker import Faker
from email_marketing_feature_app.models import Email

class Command(BaseCommand):
    help = 'Create email records in the database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_emails', type=int, nargs='?', default=10)

    def handle(self, *args, **options):
        number_of_emails = options['number_of_emails']
        fake = Faker()

        for _ in range(number_of_emails):
            new_email = Email.objects.create(
                subject=fake.sentence(nb_words=6),
                title=fake.sentence(nb_words=4),
                content='<p>This is a test</p><p><strong>Just to test purposes</strong></p>'
            )

            self.stdout.write(self.style.SUCCESS(f'Email "{new_email}" created'))

        print(f'"{len(Email.objects.all())}" email records created')
