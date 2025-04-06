from django.urls import path
from .views import crypto_list, add_to_watchlist, remove_from_watchlist, set_price_alert, check_price_alerts, delete_alert

urlpatterns = [
    path('', crypto_list, name='crypto_list'),
    path('add/<int:crypto_id>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove/<int:crypto_id>/', remove_from_watchlist, name='remove_from_watchlist'),
    path('set_alert/<int:crypto_id>/', set_price_alert, name='set_price_alert'),
    path('check_alerts/', check_price_alerts, name='check_price_alerts'),
    path('delete_alert/<int:alert_id>/', delete_alert, name='delete_alert'),
]