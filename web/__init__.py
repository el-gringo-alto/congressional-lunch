from flask import Flask, render_template, request, abort, json

from .utils import *



app = Flask(__name__)


@app.context_processor
def inject_variables():
    return dict(copyright_year = datetime.now().year,
                current_time = datetime.now().strftime('%I:%M %p'),
                current_date = datetime.now().strftime('%b %d, %Y'),
                rand_retweets = random.randint(0, 999),
                rand_likes = random.randint(0, 999))


@app.route('/')
def index():
    party = request.args.get('party')
    header = request.args.get('header')
    try:
        return render_template('index.html', header_visable=header)
    except IndexError:
        abort(404)


@app.route('/tile')
def tile():
    party = request.args.get('party')
    header = request.args.get('header')
    try:
        return render_template('tile.html', header_visable=header)
    except IndexError:
        abort(404)


@app.route('/stream')
def stream():
    party = request.args.get('party')
    if party and party.lower() == 'republican':
        sql = 'SELECT * FROM tweets WHERE party="Republican" OR party="Libertarian" ORDER BY id DESC LIMIT 50'
    elif party and party.lower() == 'democratic':
        sql = 'SELECT * FROM tweets WHERE party="Democratic" OR party="Independent" ORDER BY id DESC LIMIT 50'
    else:
        sql = 'SELECT * FROM tweets ORDER BY id DESC LIMIT 50'

    tweets = sql_query(sql)
    resp = app.response_class(
        response=json.dumps(tweets),
        status=200,
        mimetype='application/json'
    )
    try:
        return resp
    except IndexError:
        abort(404)


@app.route('/<int:tweet_id>')
def single_tweet(tweet_id):
    tweet_content = sql_query('SELECT * FROM tweets WHERE id = %s', (tweet_id,))
    try:
        return render_template('single.html', title='Single Tweet', tweet_content=tweet_content)
    except IndexError:
        abort(404)


@app.route('/random')
def random_tweet():
    tweet_content = sql_query('SELECT * FROM tweets ORDER BY RAND() LIMIT 1')
    try:
        return render_template('single.html', title='Random Tweet', tweet_content=tweet_content)
    except IndexError:
        abort(404)


@app.route('/about')
def about():
    about_txt = 'Tweets generated through machine learning using tweets from a congressman&apos;s own party. These tweets are fake and do not represent the views nor beliefs of the person they are credited to. <a href="http://samschultheis.com">#PersonalWebsite</a>'
    try:
        return render_template('message.html', title='About', msg=about_txt)
    except IndexError:
        abort(404)


@app.route('/error/404')
def error404():
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    error_msg = '404 Page Not Found'
    return render_template('message.html', title=error_msg, msg=error_msg), 404


@app.route('/error/500')
def error500():
    abort(500)

@app.errorhandler(500)
def internal_error(error):
    error_msg = '500 Internal Server Error'
    return render_template('message.html', title=error_msg, msg=error_msg), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
