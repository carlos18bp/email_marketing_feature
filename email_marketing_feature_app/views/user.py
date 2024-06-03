from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from email_marketing_feature_app.models import User
from email_marketing_feature_app.serializers import UserSerializer

@api_view(['GET'])
def user_list(request):
    """
    Handles GET requests to list all User records.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The HTTP response with the list of User records.
    """
    users = User.objects.all().order_by('-created_at')
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
