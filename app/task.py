# myapp/tasks.py

from app.celery import shared_task
from django.conf import settings
from .models import Subscription, DeviceToken
import requests
from firebase_admin import messaging

@shared_task
def check_prices_and_notify():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        symbol = subscription.symbol.name
        threshold_price = subscription.threshold_price

        response = requests.get(f'https://api.example.com/price?symbol={symbol}')
        data = response.json()
        current_price = data['price']

        if current_price >= threshold_price:
            user = subscription.user
            device_tokens = DeviceToken.objects.filter(user=user)

            for device_token in device_tokens:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title='Price Alert Notification',
                        body=f'The price of {symbol} has reached {current_price}, which is above your threshold of {threshold_price}.'
                    ),
                    token=device_token.token,
                )

                response = messaging.send(message)
                print('Successfully sent message:', response)
