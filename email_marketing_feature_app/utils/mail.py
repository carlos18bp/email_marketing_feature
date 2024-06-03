from django.core.mail import EmailMessage
from django.conf import settings
from email.mime.image import MIMEImage

def send_email(subject, message, images, users_emails):
    """
    Sends an email with embedded images to a list of users.
    
    Args:
        subject (str): The subject of the email.
        message (str): The HTML content of the email.
        images (list): A list of tuples containing image name, image data, and content ID.
        users_emails (list): A list of email addresses to send the email to.
        
    Returns:
        None
    """
    email_from = settings.EMAIL_HOST_USER
    #recipient_list = users_emails  # You can adjust the recipient list as needed
    # For testing purposes, the recipient list is hardcoded
    recipient_list = ['misfotoscmbp@gmail.com']
    
    # Create the email
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.content_subtype = "html"  # Set the email to send HTML content

    # Attach images
    for img_name, img_data, cid in images:
        image = MIMEImage(img_data)
        image.add_header('Content-ID', f'<{img_name}>')
        image.add_header('Content-Disposition', 'inline', filename=img_name)
        email.attach(image)
    
    email.send()
