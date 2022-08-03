import json
import random

from flask import render_template, request, Response

from web import app
from .utils import *



@app.route('/')
def index():
    '''
    Displays a stream of the last 10 created tweets.
    '''
    party = request.args.get('party')
    header = request.args.get('header')
    if party and party.lower() == 'republican':
        sql = '''SELECT * FROM tweets
                 WHERE (party="Republican" OR party="Libertarian")
                 ORDER BY id DESC LIMIT 10'''
    elif party and party.lower() == 'democratic':
        sql = '''SELECT * FROM tweets
                 WHERE (party="Democratic" OR party="Independent")
                 ORDER BY id DESC LIMIT 10'''
    else:
        sql = 'SELECT * FROM tweets ORDER BY id DESC LIMIT 10'

    tweets = sql_query(sql)
    return render_template('index.html.j2', header_visable=header, tweets=tweets)


@app.route('/tile')
def tile():
    '''
    Displays a tile version of the index page.
    '''
    party = request.args.get('party')
    header = request.args.get('header')
    if party and party.lower() == 'republican':
        sql = '''SELECT * FROM tweets
                 WHERE (party="Republican" OR party="Libertarian")
                 ORDER BY id DESC LIMIT 30'''
    elif party and party.lower() == 'democratic':
        sql = '''SELECT * FROM tweets
                 WHERE (party="Democratic" OR party="Independent")
                 ORDER BY id DESC LIMIT 30'''
    else:
        sql = 'SELECT * FROM tweets ORDER BY id DESC LIMIT 30'

    tweets = sql_query(sql)
    return render_template('tile.html.j2', header_visable=header, tweets=tweets)


@app.route('/stream')
def stream():
    '''
    Server Side Event to push newly created tweets to the stream.
    TODO: Send html instead of json so it's rendered server side.
    '''
    party = request.args.get('party')
    if party and party.lower() == 'republican':
        cur_tweet = sql_query('''SELECT id FROM tweets
                                 WHERE (party="Republican" OR party="Libertarian")
                                 ORDER BY id DESC LIMIT 1''')
        sql = '''SELECT * FROM tweets
                 WHERE party="Republican" OR party="Libertarian"
                 ORDER BY id DESC LIMIT 1'''
    elif party and party.lower() == 'democratic':
        cur_tweet = sql_query('''SELECT id FROM tweets
                                 WHERE (party="Democratic" OR party="Independent")
                                 ORDER BY id DESC LIMIT 1''')
        sql = '''SELECT * FROM tweets
                 WHERE party="Democratic" OR party="Independent"
                 ORDER BY id DESC LIMIT 1'''
    else:
        cur_tweet = sql_query('SELECT id FROM tweets ORDER BY id DESC LIMIT 1')
        sql = 'SELECT * FROM tweets ORDER BY id DESC LIMIT 1'

    def event_stream():
        '''
        Get the latest tweet from the database and see if it needs to be updated on the client.
        '''
        prev_tweet_id = cur_tweet[0]['id']
        while True:
            tweet = sql_query(sql)
            if tweet[0]['id'] != prev_tweet_id:
                prev_tweet_id = tweet[0]['id']
                yield f"data:{json.dumps(tweet[0])}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/stream-cont')
def stream_cont():
    party = request.args.get('party')
    last_id = request.args.get('id')
    if not last_id:
        abort(500)
    if party and party.lower() == 'republican':
        tweets = sql_query('''SELECT *
                              FROM tweets
                              WHERE (party="Republican" OR party="Libertarian")
                              AND (id < %s)
                              ORDER BY id DESC LIMIT 10''', (last_id,))
    elif party and party.lower() == 'democratic':
        tweets = sql_query('''SELECT *
                              FROM tweets
                              WHERE (party="Democratic" OR party="Independent")
                              AND (id < %s)
                              ORDER BY id DESC LIMIT 10''', (last_id,))
    else:
        tweets = sql_query('''SELECT *
                              FROM tweets
                              WHERE ( id < %s )
                              ORDER BY id
                              DESC LIMIT 10''', (last_id,))
    return app.response_class(
        response=json.dumps(tweets),
        status=200,
        mimetype='application/json'
    )


@app.route('/tweet/<int:tweet_id>')
def single_tweet(tweet_id):
    '''
    Displays a single tweet specified by its id.
    '''
    tweet_content = sql_query('SELECT * FROM tweets WHERE id = %s', (tweet_id,))
    return render_template('single.html.j2', title='Single Tweet', tweet_content=tweet_content)


@app.route('/random')
def random_tweet():
    '''
    Displays a single random tweet.
    '''
    tweet_content = sql_query('SELECT * FROM tweets ORDER BY RAND() LIMIT 1')
    return render_template('single.html.j2', title='Random Tweet', tweet_content=tweet_content)


@app.route('/about')
def about():
    '''
    Displays an about me page.
    '''
    about_txt = 'Tweets generated through machine learning using tweets from a congressman&apos;s own party. These tweets are fake and do not represent the views nor beliefs of the person they are credited to. <a href="http://samschultheis.com" target="_blank">#PersonalWebsite</a> <a href="https://github.com/el-gringo-alto/congressional-lunch" target="_blank">#GithubRepo</a>'
    return render_template('message.html.j2', title='About', msg=about_txt)


@app.route('/error/404')
def error404():
    '''
    Displays 404 error page.
    '''
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    '''
    Handles 404 errors.
    '''
    error_msg = '404 Page Not Found'
    return render_template('message.html.j2', title=error_msg, msg=error_msg), 404


@app.route('/error/500')
def error500():
    '''
    Displays 500 error page.
    '''
    abort(500)

@app.errorhandler(500)
def internal_error(error):
    '''
    Handles 500 errors.
    '''
    error_msg = '500 Internal Server Error'
    return render_template('message.html.j2', title=error_msg, msg=error_msg), 500
