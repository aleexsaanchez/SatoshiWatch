from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
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

def home(request):
    return render(request, 'watchlist/home.html')

def crypto_list(request):
    cryptos = Cryptocurrency.objects.all()
    watchlist = CryptoWatchlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    watchlist_ids = [item.crypto.id for item in watchlist]
    return render(request, 'watchlist/crypto_list.html', {'cryptos': cryptos, 'watchlist_ids': watchlist_ids})

@login_required
def watchlist(request):
    print(f"Logged-in user: {request.user.username}")
    watchlist = CryptoWatchlist.objects.filter(user=request.user)
    print(f"Watchlist entries: {watchlist}")
    return render(request, 'watchlist/watchlist.html', {'watchlist': watchlist})

@login_required
def add_to_watchlist(request, crypto_id):
    if request.method == 'POST':
        crypto = Cryptocurrency.objects.get(id=crypto_id)
        watchlist_item, created = CryptoWatchlist.objects.get_or_create(user=request.user, crypto=crypto)
        if created:
            print(f"Added {crypto.name} to watchlist for {request.user.username}")
        else:
            print(f"{crypto.name} already in watchlist for {request.user.username}")
    return redirect('crypto_list')

@login_required
def remove_from_watchlist(request, crypto_id):
    CryptoWatchlist.objects.filter(user=request.user, crypto_id=crypto_id).delete()
    return redirect('watchlist')


def home(request):
    top_cryptos = get_top_cryptos()[:3]  # Top 3 from API
    return render(request, 'watchlist/home.html', {'top_cryptos': top_cryptos})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Auto login after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'watchlist/signup.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')