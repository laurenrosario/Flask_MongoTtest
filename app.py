from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import pytz
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import products

app = Flask(__name__)
app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://3.19.240.27:27017/lr_engine"
mongo = PyMongo(app)


def setup_cron(function):
    """Set up the cron job run my AP Scheduler"""
    sched = BackgroundScheduler()
    sched.add_job(function, 'cron', hour=15, minute=42)
    print('set last time run')
    sched.add_job(set_last_time_run, 'cron', hour=15, minute=42,
                  timezone=pytz.timezone('US/Eastern'))
    sched.start()
    sched.print_jobs()


last_time_run = ''


def set_last_time_run():
    print('this is getting called')
    global last_time_run
    last_time_run = datetime.datetime.now()


@app.route('/')
def root():
    return f'Last inventory refresh was at {last_time_run}'


setup_cron(products.get_product_inventory)

if __name__ == "__main__":
    app.run()
