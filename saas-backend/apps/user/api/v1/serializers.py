
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.core.commons.dynamic_serializers import DynamicFieldsModelSerializer
from apps.user.utils import get_jwt_response
from apps.user.services import register_user
User = get_user_model()

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    organization_name = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'organization_name']

    def create(self, validated_data):
        return register_user(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(get_jwt_response(self.user))
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    