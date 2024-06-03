from rest_framework import serializers
from email_marketing_feature_app.models import Email

class EmailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Email model.
    """
    class Meta:
        model = Email
        fields = ['id', 'title', 'subject', 'content', 'created_at', 'updated_at']