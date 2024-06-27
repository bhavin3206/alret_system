from django.db import models
from django.contrib.auth.models import User

class Symbol(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="Symbol Name")

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='subscriptions')
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Threshold Price")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.user.username} - {self.symbol.name} - {self.threshold_price}"

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
