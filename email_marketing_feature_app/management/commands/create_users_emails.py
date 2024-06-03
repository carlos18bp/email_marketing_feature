from django.core.management.base import BaseCommand
from faker import Faker
from email_marketing_feature_app.models import User, Email, UserEmail
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create user-email relationship records in the database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users_emails', type=int, nargs='?', default=10)

    def handle(self, *args, **options):
        number_of_records = options['number_of_users_emails']
        fake = Faker()

        users = list(User.objects.all())
        emails = list(Email.objects.all())

        if not users or not emails:
            self.stdout.write(self.style.ERROR('There must be users and emails in the database to create UserEmail records'))
            return

        for _ in range(number_of_records):
            user = fake.random_element(users)
            email = fake.random_element(emails)
            sent = fake.boolean()
            if sent:
                scheduled_date = timezone.now()
                sent_date = timezone.now()
            else:
                scheduled_date = timezone.now() + timedelta(days=fake.random_int(min=1, max=10))
                sent_date = None

            new_user_email = UserEmail.objects.create(
                user=user,
                email=email,
                scheduled_date=scheduled_date,
                sent=sent,
                sent_date=sent_date
            )

            self.stdout.write(self.style.SUCCESS(f'UserEmail "{new_user_email}" created'))

        print(f'"{len(UserEmail.objects.all())}" user-email records created')
