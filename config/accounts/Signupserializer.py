from rest_framework import serializer
from .models import CustomUser


class SignupSerializer(serializer.ModelSerializer):
    password1 = serializer.CharField(write_only=True)
    password2 = serializer.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'display_name',
            'password1',
            'password2',
        ]

        def validate(self, attrs):

            if attrs["password"] != attrs["password2"]:
                raise serializer.ValidationError(
                    {"password2": "パスワードが一致しません"}
                )

            return attrs
        
    def create(self, validated_data):#password2がDBに存在しないとは？一連の解説。そもそもserializerとは？

        validated_data.pop("password2")

        user = CustomUser(
            email=validated_data["email"],
            display_name=validated_data.get("display_name", "")
        )

        user.set_password(validated_data["password"])
        user.save()

        return user