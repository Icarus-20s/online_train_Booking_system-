from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, Ticket, hash_raw_password  # Import the hash_raw_password function


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)

        if confirm_password and confirm_password != password:
            raise ValidationError({"password": "Passwords must match."})

        validated_data['password'] = hash_raw_password(password)
        user = User.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        confirm_password = attrs.get("confirm_password", None)
        password = attrs.get("password", None)
        if confirm_password and confirm_password != password:
            raise ValidationError("password and confirm_password should match")
        return super().validate(attrs)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
