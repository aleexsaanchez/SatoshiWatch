from django.db import models
from django.contrib.auth.models import User

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    price_usd = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap = models.BigIntegerField()

    def __str__(self):
        return self.name

class CryptoWatchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto.name} ({self.user.username})"
    
class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_triggered = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.crypto} at ${self.target_price} by {self.user.username}"
    
    