from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from email_marketing_feature_app.models import Email, User, UserEmail
from email_marketing_feature_app.serializers import EmailSerializer
from email_marketing_feature_app.utils.handle_images import handle_images
from email_marketing_feature_app.tasks import send_email_task
from datetime import datetime

@api_view(['GET', 'POST'])
def email_list_create(request):
    """
    Handles GET and POST requests for the email list and creation of new emails.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The HTTP response with the email data or error.
    """
    if request.method == 'GET':
        emails = Email.objects.all().order_by('-created_at')
        serializer = EmailSerializer(emails, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        data = request.data.copy()
        content = data.get('content', '')

        # Handle embedded images
        content, content_with_cid, images = handle_images(content)
        data['content'] = content

        serializer = EmailSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            email = serializer.save()
            # Call the Celery task to send the email
            # send_email_task.delay(email.subject, content_with_cid, images)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def email_update(request, id):
    """
    Handles PUT requests to update an existing email.

    Args:
        request: The HTTP request object.
        id: The ID of the email to update.

    Returns:
        Response: The HTTP response with the updated email data or error.
    """
    try:
        email = Email.objects.get(id=id)
    except Email.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.dict()
    content = data.get('content', '')

    # Handle embedded images
    content, content_with_cid, images = handle_images(content)
    data['content'] = content

    serializer = EmailSerializer(email, data=data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def email_delete(request, id):
    """
    Handles DELETE requests to delete an existing email.

    Args:
        request: The HTTP request object.
        id: The ID of the email to delete.

    Returns:
        Response: The HTTP response indicating the result of the deletion.
    """
    try:
        email = Email.objects.get(id=id)
        email.delete()
        return Response(status=status.HTTP_200_OK)
    except Email.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def send_email_to_users(request):
    """
    Handles POST requests to send emails to selected users.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The HTTP response indicating the result of the email sending process.
    """
    email_id = request.data.get('email_id')
    user_ids = request.data.get('user_ids', [])
    email = Email.objects.get(id=email_id)
    users = User.objects.filter(id__in=user_ids)
    if not users:
        return Response({"detail": "No users selected"}, status=status.HTTP_400_BAD_REQUEST)
    
    for user in users:
        UserEmail.objects.create(user=user, email=email, scheduled_date=datetime.now(), sent_date=datetime.now(), sent=True)

    users_emails = list(users.values_list('email', flat=True))

    # Handle embedded images
    content, content_with_cid, images = handle_images(email.content)
    # send_email_task.delay(email.subject, content_with_cid, images, users_emails)
    
    return Response({"detail": "Emails are being sent"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def schedule_email(request):
    """
    Handles POST requests to schedule emails to selected users at a specified date.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The HTTP response indicating the result of the scheduling process.
    """
    email_id = request.data.get('email_id')
    user_ids = request.data.get('user_ids', [])
    scheduled_date = request.data.get('scheduled_date')

    try:
        scheduled_date = datetime.fromisoformat(scheduled_date)
    except ValueError:
        return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    email = Email.objects.get(id=email_id)
    users = User.objects.filter(id__in=user_ids)

    for user in users:
        UserEmail.objects.create(user=user, email=email, scheduled_date=scheduled_date)
    
    return Response({"detail": "Emails scheduled"}, status=status.HTTP_201_CREATED)
