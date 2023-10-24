from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import TempUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, min_length=8)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'date_joined', 'last_active')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

class TempUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempUser
        fields = ['email', 'password']

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

