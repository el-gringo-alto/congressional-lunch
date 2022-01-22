'''
Utility functions and classes.
'''
import configparser

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


class Config:
    '''
    App configuration.
    '''
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'America/New_York'
