import requests
from django.core.management.base import BaseCommand  # Correct import
from watchlist.models import Cryptocurrency

class Command(BaseCommand):  # Correct class name
    help = 'Fetches cryptocurrency data from CoinGecko and updates the database'

    def handle(self, *args, **kwargs):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 50,
            'page': 1,
            'sparkline': False
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            for crypto in data:
                Cryptocurrency.objects.update_or_create(
                    name=crypto['name'],
                    defaults={
                        'symbol': crypto['symbol'],
                        'price_usd': crypto.get('current_price', 0),
                        'market_cap': crypto.get('market_cap', 0),
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Updated {crypto['name']}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data: {e}"))