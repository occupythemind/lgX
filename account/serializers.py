from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = Account
        fields = ("id", "email", "password")

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"
    
    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs.get("email").lower(),
            password=attrs.get("password"),
        )
        if not user:
            raise AuthenticationFailed(settings.MSG_INVALID_CRED)

        if not user.is_active:
            raise AuthenticationFailed(settings.MSG_ACCOUNT_DISABLED)

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


