import configparser
from datetime import datetime
import random


from flask import abort
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



def sql_query(query: str, vals=()) -> dict:
    """
    Input a SQL query and return a dictionary of results.
    """
    config = configparser.ConfigParser()
    config.read('keys.ini')

    conn =  mysql.connector.connect(**config['database'], raise_on_warnings=False)
    cur = conn.cursor(dictionary=True)

    cur.execute(query, vals)

    resp = cur.fetchall()
    conn.commit()

    cur.close()
    conn.close()

    if resp is None:
        abort(500)

    return resp
