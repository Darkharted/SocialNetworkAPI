from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from .tasks import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4, required=True, write_only=True
    )
    password_confim = serializers.CharField(
        min_length=4, required=True,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password',
            'password_confim'
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confim = attrs.pop('password_confim')
        if password != password_confim:
            msg_ = (
                "Passwords do not match"
            )
            raise serializers.ValidationError(msg_)
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code(
            user.email, user.activation_code
        )
        return user

