from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Symbol, Subscription, DeviceToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'validators': []}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'name']


class SubscriptionSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField()

    class Meta:
        model = Subscription
        fields = ['id', 'symbol', 'threshold_price']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        symbol_name = validated_data.pop('symbol')

        symbol, created = Symbol.objects.get_or_create(name=symbol_name)
        subscription = Subscription.objects.create(user=request.user, symbol=symbol, **validated_data)
        return subscription

    def validate_symbol(self, value):
        if not Symbol.objects.filter(name=value).exists():
            Symbol.objects.create(name=value)
        return value


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['token']

    def create(self, validated_data):
        request = self.context.get('request')
        token = validated_data.get('token')
        user = request.user

        device_token, created = DeviceToken.objects.get_or_create(user=user, token=token)
        if not created:
            raise serializers.ValidationError("This device token already exists for the user.")
        return device_token
