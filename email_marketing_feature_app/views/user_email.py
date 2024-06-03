from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from email_marketing_feature_app.models import UserEmail
from email_marketing_feature_app.serializers import UserEmailSerializer

@api_view(['GET'])
def users_emails_list(request):
    """
    Handles GET requests to list all UserEmail records.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The HTTP response with the list of UserEmail records.
    """
    users_emails = UserEmail.objects.all().order_by('-created_at')
    serializer = UserEmailSerializer(users_emails, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_scheduled_email(request, id):
    """
    Handles DELETE requests to delete a scheduled email by its ID.

    Args:
        request: The HTTP request object.
        id: The ID of the scheduled email to delete.

    Returns:
        Response: The HTTP response indicating the result of the deletion.
    """
    try:
        user_email = UserEmail.objects.get(pk=id)
        user_email.delete()
        return Response({"detail": "Scheduled email deleted"}, status=status.HTTP_200_OK)
    except UserEmail.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
