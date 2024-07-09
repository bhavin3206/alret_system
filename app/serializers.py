from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *

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
        model = SymbolData
        fields = ['instrument_token', 'tradingsymbol', 'name', 'expiry', 'exchange', 'segment', 'instrument_type']


class SubscriptionSerializer(serializers.ModelSerializer):
    instrument_token = serializers.CharField(write_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'instrument_token', 'threshold_price']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        instrument_token = validated_data.pop('instrument_token')

        try:
            symbol = SymbolData.objects.get(instrument_token=instrument_token)
        except SymbolData.DoesNotExist:
            raise serializers.ValidationError("Symbol with the given instrument token does not exist.")

        if Subscription.objects.filter(user=request.user, symbol=symbol).exists():
            raise serializers.ValidationError("Subscription with this instrument token already exists.")

        if not request.user.is_superuser and Subscription.objects.filter(user=request.user).count() >= 2:
            raise serializers.ValidationError("Your subscription limit has been reached. Please try again tomorrow.")

        subscription = Subscription.objects.create(user=request.user, symbol=symbol, **validated_data)
        return subscription

    def validate_instrument_token(self, value):
        if not SymbolData.objects.filter(instrument_token=value).exists():
            raise serializers.ValidationError("Invalid instrument token.")
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
