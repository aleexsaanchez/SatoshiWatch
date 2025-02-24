from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from watchlist.models import Cryptocurrency, CryptoWatchlist
import requests

def get_top_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

def crypto_list(request):
    # Fetch real-time data
    api_cryptos = get_top_cryptos()
    # Update database (optional, for consistency)
    for crypto in api_cryptos:
        Cryptocurrency.objects.update_or_create(
            name=crypto['name'],
            defaults={
                'symbol': crypto['symbol'],
                'price_usd': crypto.get('current_price', 0),
                'market_cap': crypto.get('market_cap', 0),
            }
        )
    cryptos = Cryptocurrency.objects.all()
    watchlist = CryptoWatchlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    watchlist_ids = [item.crypto.id for item in watchlist]
    return render(request, 'watchlist/crypto_list.html', {'cryptos': cryptos, 'watchlist_ids': watchlist_ids})

@login_required
def add_to_watchlist(request, crypto_id):
    crypto = Cryptocurrency.objects.get(id=crypto_id)
    CryptoWatchlist.objects.get_or_create(user=request.user, crypto=crypto)
    return redirect('crypto_list')

@login_required
def remove_from_watchlist(request, crypto_id):
    CryptoWatchlist.objects.filter(user=request.user, crypto_id=crypto_id).delete()
    return redirect('crypto_list')