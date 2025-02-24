from django.urls import path
from .views import crypto_list

urlpatterns = [
    path('', crypto_list, name='crypto_list'),  # Accessible at /cryptos/
]

