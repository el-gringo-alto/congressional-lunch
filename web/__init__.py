from datetime import datetime
import json
import random

from flask import Flask, render_template, request, Response
from flask_apscheduler import APScheduler

from .cron import gen_tweet, scrape_data
from .utils import *



# initialize flask
app = Flask(__name__)
app.config.from_object(Config())


# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Generate a tweet every 5 minutes
scheduler.add_job(func=gen_tweet, trigger='cron', id='do_gen_tweet', minute='*/5')

# Scrape Twitter for data every 8 hours
scheduler.add_job(func=scrape_data, trigger='cron', id='do_scrape_data', hour='*/8')


@app.context_processor
def inject_variables():
    '''
    Dynamic variables to be passed to templates.
    '''
    return dict(copyright_year = datetime.now().year,
                current_time = datetime.now().strftime('%I:%M %p'),
                current_date = datetime.now().strftime('%b %d, %Y'),
                rand_retweets = random.randint(0, 999),
                rand_likes = random.randint(0, 999))


import web.views


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
