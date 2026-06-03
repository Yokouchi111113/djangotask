from rest_framework import serializers
from django.contrib.auth import authenticate


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def validate(self, attrs):
        #ひとまずusernameで試す
        user = authenticate(
            username=attrs["email"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError(
                "メールアドレスまたはパスワードが正しくありません"
            )
        #viewsで取り出せる
        attrs["user"] = user

        return attrs