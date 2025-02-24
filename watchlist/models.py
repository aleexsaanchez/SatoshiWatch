from django.db import models

# Create your models here.
class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    price_usd = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap = models.BigIntegerField()
    
    def __str__(self):
        return self.name