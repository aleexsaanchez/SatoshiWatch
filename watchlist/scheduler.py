# watchlist/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from watchlist.views import update_crypto_prices

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        update_crypto_prices,
        'interval',
        minutes=5,  # Update every 5 minutes
        id='update_crypto_prices',
        replace_existing=True
    )
    scheduler.start()