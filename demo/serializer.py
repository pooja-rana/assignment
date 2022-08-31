from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from .models import UserDetail


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, max_length=68, min_length=6, write_only=True,
                                     validators=[validate_password])
    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=50,
        validators=[UniqueValidator(queryset=UserDetail.objects.all(), )
                    ])

    class Meta:
        model = UserDetail
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'roles']

    def create(self, validated_data):
        userdetail = UserDetail.objects.create_user(email=validated_data['email'],
                                                    username=validated_data['username'],
                                                    first_name=validated_data['first_name'],
                                                    last_name=validated_data['last_name'],
                                                    roles=validated_data['roles'])
        print(userdetail)
        userdetail.set_password(validated_data['password'])
        userdetail.save()
        return userdetail

    def update(self, validated_data, pk):
        user_details = UserDetail.objects.filter(id=pk)

        user_details.update()
        return user_details


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, style={'input_type':'password'}, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = UserDetail.objects.get(email=obj["email"])

        return {
            "access": user.tokens()["access"],
            "refresh": user.tokens()["refresh"]
        }

    class Meta:
        model = UserDetail
        fields = ("email", "password", "tokens")

    def validate(self, attrs):

        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)


        return {
            "email": user.email,
            "tokens": user.tokens
        }
