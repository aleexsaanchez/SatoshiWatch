from django.urls import path
from .views import crypto_list, add_to_watchlist, remove_from_watchlist

urlpatterns = [
    path('', crypto_list, name='crypto_list'),
    path('add/<int:crypto_id>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove/<int:crypto_id>/', remove_from_watchlist, name='remove_from_watchlist'),
]
