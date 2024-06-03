from rest_framework import serializers
from email_marketing_feature_app.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_admin']