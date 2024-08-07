from django.db import models
from django.contrib.auth.models import User

class SymbolData(models.Model):
    instrument_token = models.CharField(max_length=50, unique=True)
    tradingsymbol = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    expiry = models.DateField(null=True, blank=True)  # Assuming expiry is a date field
    exchange = models.CharField(max_length=50)
    segment = models.CharField(max_length=50)
    instrument_type = models.CharField(max_length=50)

    def _str_(self):
        return f"{self.tradingsymbol} - {self.name}"

    class Meta:
        verbose_name = "Trading Instrument"
        verbose_name_plural = "Trading Instruments"
        ordering = ['expiry']

class Subscription(models.Model):
    SMS = 'SMS'
    EMAIL = 'Email'
    NOTIFICATION = 'Notification'

    ALERT_TYPE_CHOICES = [
        (SMS, 'SMS'),
        (EMAIL, 'Email'),
        (NOTIFICATION, 'Notification'),
    ]

    GREATER_THAN = '>'
    LESS_THAN = '<'

    LOREM_QUESTION_CHOICES = [
        (GREATER_THAN, 'Greater than'),
        (LESS_THAN, 'Less than'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    symbol = models.ForeignKey(SymbolData, on_delete=models.CASCADE, related_name='subscriptions')
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Threshold Price")
    alert_type = models.CharField(max_length=15, choices=ALERT_TYPE_CHOICES, default=NOTIFICATION, verbose_name="Alert Type")
    lorem_question = models.CharField(max_length=1, choices=LOREM_QUESTION_CHOICES, default=GREATER_THAN, verbose_name="Lorem Question")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.user.username} - {self.symbol.name} - {self.threshold_price} - {self.alert_type} - {self.lorem_question}"

    class Meta:
        unique_together = ('user', 'symbol')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['symbol']),
        ]

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255, unique=True, verbose_name="Device Token")

    def __str__(self):
        return f"{self.user.username} - {self.token}"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



