# watchlist/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from watchlist.models import Cryptocurrency, CryptoWatchlist, PriceAlert
from watchlist.forms import PriceAlertForm
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
    top_cryptos = get_top_cryptos()[:3]  # Top 3 from API
    return render(request, 'watchlist/home.html', {'top_cryptos': top_cryptos})

def crypto_list(request):
    cryptos = Cryptocurrency.objects.all()
    watchlist = CryptoWatchlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    watchlist_ids = [item.crypto.id for item in watchlist]
    form = PriceAlertForm()  # Pass the form to the template
    return render(request, 'watchlist/crypto_list.html', {
        'cryptos': cryptos,
        'watchlist_ids': watchlist_ids,
        'form': form
    })

@login_required
def watchlist(request):
    print(f"Logged-in user: {request.user.username}")
    watchlist = CryptoWatchlist.objects.filter(user=request.user)
    print(f"Watchlist entries: {watchlist}")
    form = PriceAlertForm()  # Add the form
    return render(request, 'watchlist/watchlist.html', {
        'watchlist': watchlist,
        'form': form
    })

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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'watchlist/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def set_price_alert(request, crypto_id):
    crypto = Cryptocurrency.objects.get(id=crypto_id)
    if request.method == 'POST':
        form = PriceAlertForm(request.POST)
        if form.is_valid():
            price_alert = form.save(commit=False)
            price_alert.user = request.user
            price_alert.crypto = crypto
            price_alert.save()
            return redirect('crypto_list')
    else:
        form = PriceAlertForm()
    return render(request, 'watchlist/crypto_list.html', {
        'cryptos': Cryptocurrency.objects.all(),
        'watchlist_ids': [item.crypto.id for item in CryptoWatchlist.objects.filter(user=request.user)] if request.user.is_authenticated else [],
        'form': form
    })

@login_required
def check_price_alerts(request):
    # Check for triggered alerts
    alerts_to_check = PriceAlert.objects.filter(user=request.user, is_triggered=False)
    triggered_alerts = []
    for alert in alerts_to_check:
        current_price = float(alert.crypto.price_usd)
        if current_price >= float(alert.target_price):
            alert.is_triggered = True
            alert.save()
            triggered_alerts.append(f"{alert.crypto.name} has reached ${alert.target_price}!")

    # Fetch all alerts for display
    all_alerts = PriceAlert.objects.filter(user=request.user)
    return render(request, 'watchlist/notifications.html', {
        'triggered_alerts': triggered_alerts,
        'all_alerts': all_alerts
    })

@login_required
def delete_alert(request, alert_id):
    PriceAlert.objects.filter(id=alert_id, user=request.user).delete()
    return redirect('check_price_alerts')