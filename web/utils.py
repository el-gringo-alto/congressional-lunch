import configparser
from datetime import datetime
import random


import mysql.connector



personal_content = [{
    'id': None,
    'tweet': '',
    'name': 'Sam Schultheis',
    'handle': 'SamSchultheis',
    'party': 'Democratic',
    'retweets': random.randint(0, 999),
    'likes': random.randint(0, 999),
    'time': datetime.now().strftime('%I:%M %p'),
    'date': datetime.now().strftime('%b %d, %Y')}]



def sql_query(query, vars=()):
    # keys_file = pathlib.Path('keys.ini')
    config = configparser.ConfigParser()
    config.read('keys.ini')

    db = mysql.connector.connect(**config['database'], raise_on_warnings=False)
    cur = db.cursor(dictionary=True)

    cur.execute(query, vars)

    tweet = cur.fetchall()
    db.commit()

    cur.close()
    db.close()

    if tweet is None:
        abort(404)
    return tweet
