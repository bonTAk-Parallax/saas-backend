
# apps/users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.user.utils import get_jwt_response

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Override the default response with our rich payload
        return get_jwt_response(self.user)