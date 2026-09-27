
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.core.commons.dynamic_serializers import DynamicFieldsModelSerializer
from apps.user.utils import get_jwt_response
from apps.user.services import register_user, register_user_via_invite
User = get_user_model()

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    organization_name = serializers.CharField(write_only=True, max_length=255)
    invite_token = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'organization_name', 'invite_token']

    def validate(self, attrs):
        has_org_name = bool(attrs.get('organization_name'))
        has_invite = bool(attrs.get('invite_token'))
        if has_org_name == has_invite: 
            raise serializers.ValidationError(
                "Provide exactly one of organization_name (new company) or invite_token (joining an existing one)."
            )
        return attrs


    def create(self, validated_data):
        invite_token = validated_data.get('invite_token')
        if invite_token:
            return register_user_via_invite(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                invite_token=invite_token,
            )
        return register_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            organization_name=validated_data['organization_name'],
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(get_jwt_response(self.user))
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    