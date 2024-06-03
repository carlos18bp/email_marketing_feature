from celery import shared_task
from django.utils import timezone
from email_marketing_feature_app.models import UserEmail
from email_marketing_feature_app.utils.mail import send_email
from email_marketing_feature_app.utils.handle_images import handle_images

@shared_task
def send_email_task(subject, content_with_cid, images, users_emails):
    """
    Celery task to send an email immediately.

    Args:
        subject (str): The subject of the email.
        content_with_cid (str): The HTML content of the email with content IDs for images.
        images (list): A list of tuples containing image name, image data, and content ID.
        users_emails (list): A list of email addresses to send the email to.

    Returns:
        None
    """
    send_email(subject, content_with_cid, images, users_emails)

@shared_task
def send_scheduled_emails():
    """
    Celery task to send scheduled emails.

    Retrieves all unsent UserEmail records with a scheduled date less than or equal to the current time,
    sends the emails, and updates the records to mark them as sent.

    Args:
        None

    Returns:
        None
    """
    now = timezone.now()
    scheduled_emails = UserEmail.objects.filter(scheduled_date__lte=now, sent=False)
    
    for user_email in scheduled_emails:
        try:
            users_emails = [user_email.user.email]
            # Handle embedded images if necessary
            content_with_cid, images = handle_images(user_email.email.content)
            send_email(user_email.email.subject, content_with_cid, images, users_emails)
            user_email.sent = True
            user_email.sent_date = now
            user_email.save()
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Failed to send email to {user_email.user.email}: {e}")
