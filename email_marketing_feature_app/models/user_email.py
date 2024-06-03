from django.db import models
from email_marketing_feature_app.models import User, Email

class UserEmail(models.Model):
    """
    Model representing the many-to-many relationship between User and Email.

    Attributes:
        user (User): The user associated with the email.
        email (Email): The email associated with the user.
        scheduled_date (datetime): The date and time when the email is scheduled to be sent.
        sent (bool): Indicates whether the email has been sent. Default is False.
        sent_date (datetime): The date and time when the email was sent.
        created_at (datetime): Creation date of the email.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.email}'
