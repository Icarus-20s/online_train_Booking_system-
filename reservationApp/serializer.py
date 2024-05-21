from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def validate(self, attrs):
        confirm_password = attrs.get("confirm_password", None)
        password = attrs.get("password", None)
        if confirm_password and confirm_password != password:
            raise ValidationError("password and confirm_password should match")
        if confirm_password:
            del attrs["confirm_password"]
        return super().validate(attrs)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
