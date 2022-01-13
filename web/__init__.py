import random
from datetime import datetime

from flask import Flask, render_template, request, abort



app = Flask(__name__)

@app.context_processor
def inject_variables():
    return dict(
        copyright_year = datetime.now().year,
        current_time = datetime.now().strftime('%I:%M %p'),
        currrent_date = datetime.now().strftime('%b %d, %Y'))

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except IndexError:
        abort(404)

@app.route('/about')
def about():
    try:
        return render_template('about.html', title='About', retweets=random.randint(0, 999), likes=random.randint(0, 999))
    except IndexError:
        abort(404)

@app.route('/random')
def random_tweet():
    return render_template('about.html', title='About', retweets='59', likes='423')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# @app.route('/stream')
# def stream():
#     if request.method == 'POST':
#         print("Data received from Webhook is: ", request.json)
#         return 'success', 200
#     else:
#         abort(400)
#
# @app.route('/test')
# def test():
#     return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
