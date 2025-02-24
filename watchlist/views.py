from django.shortcuts import render
from watchlist.models import Cryptocurrency

def crypto_list(request):
    cryptos = Cryptocurrency.objects.all()
    return render(request, 'watchlist/crypto_list.html', {'cryptos': cryptos})
