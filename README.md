# README.md: Email Marketing Project

This project is designed for email marketing, allowing users to create, schedule, and send marketing emails. It uses Celery and Redis for background processing and scheduling tasks.

## Features

- Create, edit, and delete email posts.
- Schedule emails to be sent at a specified time.
- Send emails immediately to selected users.
- View sent and scheduled emails.
- Background processing using Celery and Redis.

## Models

### Email
- **title**: The title of the email.
- **subject**: The subject line of the email.
- **content**: The HTML content of the email.
- **created_at**: Timestamp when the email was created.
- **updated_at**: Timestamp when the email was last updated.

### User
- **first_name**: First name of the user.
- **last_name**: Last name of the user.
- **email**: Email address of the user.

### UserEmail
- **user**: Foreign key to the User model.
- **email**: Foreign key to the Email model.
- **scheduled_date**: Date when the email is scheduled to be sent.
- **sent_date**: Date when the email was actually sent.
- **sent**: Boolean indicating if the email has been sent.

## Views

### Email List
- **URL**: `/emails/`
- **Methods**: GET, POST
- **Description**: Retrieve a list of emails or create a new email.

### Email Detail
- **URL**: `/emails/<id>/`
- **Methods**: GET, PUT, DELETE
- **Description**: Retrieve, update, or delete a specific email.

### Send Email to Users
- **URL**: `/send_email_to_users/`
- **Methods**: POST
- **Description**: Send an email to selected users.

### Schedule Email
- **URL**: `/schedule_email/`
- **Methods**: POST
- **Description**: Schedule an email to be sent at a later date.

## Celery Configuration with Redis

1. **Install Redis**:
    ```bash
    sudo apt update
    sudo apt install redis-server -y
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    ```

2. **Install Celery and Django-Celery**:
    ```bash
    pip install celery django-celery-beat django-celery-results
    ```

3. **Configure Celery in Django**:
    - **email_marketing_feature_project/celery.py**:
        ```python
        from __future__ import absolute_import, unicode_literals
        import os
        from celery import Celery
        from celery.schedules import crontab

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_marketing_feature_project.settings')
        app = Celery('email_marketing_feature_project')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks()

        app.conf.beat_schedule = {
            'send-scheduled-emails-every-day': {
                'task': 'email_marketing_feature_app.tasks.send_scheduled_emails',
                'schedule': crontab(hour=12, minute=0),
            },
        }
        app.conf.timezone = 'UTC'

        @app.task(bind=True)
        def debug_task(self):
            print(f'Request: {self.request!r}')
        ```

    - **email_marketing_feature_project/settings.py**:
        ```python
        CELERY_BROKER_URL = 'redis://localhost:6379/0'
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_TIMEZONE = 'UTC'

        INSTALLED_APPS += [
            'django_celery_beat',
            'django_celery_results',
        ]

        from .celery import app as celery_app
        __all__ = ('celery_app',)
        ```

4. **Created Celery Tasks (included in the project)**:
    - **email_marketing_feature_app/tasks.py**:
        ```python
        from celery import shared_task
        from django.utils import timezone
        from email_marketing_feature_app.models import UserEmail
        from email_marketing_feature_app.utils.mail import send_email
        from email_marketing_feature_app.utils.handle_images import handle_images

        @shared_task
        def send_email_task(subject, content_with_cid, images, users_emails):
            send_email(subject, content_with_cid, images, users_emails)

        @shared_task
        def send_scheduled_emails():
            now = timezone.now()
            scheduled_emails = UserEmail.objects.filter(scheduled_date__lte=now, sent=False)
            
            for user_email in scheduled_emails:
                users_emails = [user_email.user.email]
                content_with_cid, images = handle_images(user_email.email.content)
                send_email(user_email.email.subject, content_with_cid, images, users_emails)
                user_email.sent = True
                user_email.sent_date = now
                user_email.save()
        ```

## Running the Project

1. **Start Redis**:
```bash
sudo systemctl start redis-server
```

2. **Run Celery Worker**:
```bash
celery -A email_marketing_feature_project worker --loglevel=info
```

3. **Run Celery Beat**:
```bash
celery -A email_marketing_feature_project beat --loglevel=info
```

4. **Install virtualenv**:
```bash
pip install virtualenv
```

5. **To create a new virtual env**:
```bash
virtualenv name_virtual_env
```

6. **Create virtual env**:
```bash
virtualenv email_marketing_feature_env
```

7. **Activate virtual env**:
```bash
source email_marketing_feature_env/bin/activate
```

8. **Create dependencies file**:
```bash
pip freeze > requirements.txt
```

9. **Install dependencies**:
```bash
pip install -r requirements.txt
```

10. **Desactivate virtual env**:
```bash
deactivate
```

11. **Run Run makemigrations**:
```bash
python3 manage.py makemigrations
```

12. **Run Run migrations**:
```bash
python3 manage.py migrate
```

13. **Run Create superuser**:
```bash
python3 manage.py createsuperuser
```

14. **Run Create fake data for testing purposes**:
```bash
python3 manage.py create_fake_data
```

15. **Run Django Server**:
```bash
python manage.py runserver
```

16. **Run Frontend setup**:
```bash
cd frontend
npm install
npm run dev
```