from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = CustomUser
        exclude = (
            "groups",
            "user_permissions",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "first_name",
            "last_name",
            "is_active",
            "is_active_plan",
            "username",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        user = CustomUser.all_objects.filter(email=value).first()

        if user and not user.is_deleted:
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data["email"]

        user = CustomUser.all_objects.filter(email=email).first()

        if user:
            if not user.is_deleted:
                raise serializers.ValidationError({
                    "email": "An account with this email already exists."
                })

            user.restore()

            for field, value in validated_data.items():
                setattr(user, field, value)

        else:
            user = CustomUser(**validated_data)

        user.set_password(password)
        user.last_login = timezone.now()
        user.save()

        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")

        user = CustomUser.all_objects.filter(email=email).first()

        if user and user.is_deleted:
            raise AuthenticationFailed(
                "No active account found with the given credentials"
            )

        return super().validate(attrs)