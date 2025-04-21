# watchlist/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from watchlist.models import Cryptocurrency, PriceAlert, CryptoWatchlist
from watchlist.views import update_crypto_prices

class PriceAlertTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.crypto = Cryptocurrency.objects.create(
            name='Bitcoin', symbol='btc', price_usd=50000
        )
        self.client.login(username='testuser', password='12345')

    def test_price_alert_trigger(self):
        # Set an alert
        alert = PriceAlert.objects.create(
            user=self.user,
            crypto=self.crypto,
            target_price=60000,
            is_triggered=False
        )
        # Update price to trigger alert
        self.crypto.price_usd = 70000
        self.crypto.save()
        # Check alert status
        response = self.client.get('/check_alerts/')
        alert.refresh_from_db()
        self.assertTrue(alert.is_triggered)
        self.assertContains(response, f"{self.crypto.name} has reached ${alert.target_price}!")

    def test_api_price_update(self):
        update_crypto_prices()
        self.crypto.refresh_from_db()
        self.assertNotEqual(self.crypto.price_usd, 50000)  # Price should update