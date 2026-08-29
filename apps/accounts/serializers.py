"""
Serializers for User Authentication and Profile Management.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserSession

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'avatar', 'bio', 'job_title', 'github_username',
            'gitlab_username', 'timezone', 'is_verified', 'two_factor_enabled',
            'referral_code', 'created_at'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_verified', 'created_at', 'referral_code']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm', 'referral_code']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        referral_code = validated_data.pop('referral_code', None)
        referrer = None
        if referral_code:
            referrer = User.objects.filter(referral_code=referral_code).first()
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            referred_by=referrer
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['id', 'ip_address', 'device', 'location', 'last_activity', 'is_active', 'created_at']
