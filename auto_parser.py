from celery import Celery
from celery.schedules import crontab
from pricer import parse_price

app = Celery('auto_pricer', broker='amqp://guest:guest@localhost:5672/')

@app.task
def auto_parser():
    parse_price()

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_midnight_parser' : {
        'task' : 'auto_parser.auto_parser',
        'schedule' : crontab(minute=33, hour=11),
    }
}

app.conf.timezone = 'Europe/Moscow'