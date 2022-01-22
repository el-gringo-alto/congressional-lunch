import configparser
from datetime import datetime
import random


from flask import abort
import mysql.connector



def sql_query(query: str, vals=()) -> dict:
    '''
    Input a SQL query and return a dictionary of results.
    '''
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


class APConfig:
    '''
    App configuration.
    '''
    # JOBS = [
    #     {
    #         'id': "job1",
    #         'func': "jobs:job1",
    #         'args': (1, 2),
    #         'trigger': "interval",
    #         'seconds': 10,
    #     }
    # ]
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'America/New_York'
