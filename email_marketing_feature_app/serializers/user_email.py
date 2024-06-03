from rest_framework import serializers
from email_marketing_feature_app.models import UserEmail
from email_marketing_feature_app.serializers import EmailSerializer, UserSerializer

class UserEmailSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserEmail model.
    """
    user = UserSerializer()
    email = EmailSerializer()

    class Meta:
        model = UserEmail
        fields = ['id', 'user', 'email', 'scheduled_date', 'sent', 'sent_date']