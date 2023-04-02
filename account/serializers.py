from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'created')
        extra_kwargs = {
            'email': {'read_only': True},
            'created': {'read_only': True},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField(min_length=8, max_length=64)
    password2 = serializers.CharField(min_length=8, max_length=64)

    def validate_old_password(self, data):
        user = self.context['user']
        if not user.check_password(data):
            raise serializers.ValidationError('password is wrong')
        return data

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('new passwords not match')
        return data
