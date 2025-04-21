# watchlist/apps.py
from django.apps import AppConfig

class WatchlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watchlist'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()