import os
import re
from django.db import models
from django.conf import settings

class Email(models.Model):
    """
    Model to represent an Email.

    Attributes:
        subject (str): Subject of the Email.
        title (str): Title of the Email.
        content (str): Email content in HTML format.
        created_at (datetime): Creation date of the email.
        updated_at (datetime): Last update date of the email.
    """
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """
        Deletes the Email instance and associated images.

        Overrides the delete method to remove the header image and 
        embedded images in the content before deleting the Email.
        """
        self._delete_embedded_images(self.content)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Saves the Email instance and manages associated images.

        Overrides the save method to delete the old header image and 
        embedded images if they have been modified before saving.
        """
        if self.pk:
            original = Email.objects.get(pk=self.pk)
            self._handle_content_change(original)

        super().save(*args, **kwargs)

    def _delete_embedded_images(self, content):
        """
        Deletes the embedded images in the Email content.

        Args:
            content (str): Email content in HTML format.
        """
        image_paths = re.findall(r'<img src="([^"]+)"', content)
        for path in image_paths:
            relative_path = path.replace(f'{settings.SITE_URL}/media/', '')
            image_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            self._delete_image_path(image_path)

    def _delete_image_path(self, image_path):
        """
        Deletes the image file at the specified path.

        Args:
            image_path (str): Path to the image file to delete.
        """
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except OSError as e:
                # Log the error if needed
                print(f"Error deleting file {image_path}: {e}")

    def _handle_content_change(self, original):
        """
        Manages the change of the Email content.

        Args:
            original (email): Original Email instance before changes.
        """
        if original.content != self.content:
            self._delete_embedded_images(original.content)