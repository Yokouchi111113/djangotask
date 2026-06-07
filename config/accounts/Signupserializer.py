from rest_framework import serializers
from .models import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'display_name',
            'password1',
            'password2',
        ]

    def validate(self, attrs):

        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "パスワードが一致しません"}
            )

        return attrs

    def validate_email(self, value):

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "このメールアドレスは既に登録されています"
            )

        return value


    def create(self, validated_data):

        validated_data.pop("password2")

        return CustomUser.objects.create_user(
        email=validated_data["email"],
        password=validated_data["password1"],
        display_name=validated_data.get("display_name", "")
        )