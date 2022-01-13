import random
from datetime import datetime

from flask import Flask, render_template



app = Flask(__name__)

@app.context_processor
def inject_variables():
    return dict(
        copyright_year=datetime.now().year,
        current_time=datetime.now().strftime('%I:%M %p'),
        currrent_date = datetime.now().strftime('%b %d, %Y'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About', retweets=69, likes=420)

@app.route('/random')
def random():
    return render_template('about.html', title='About', retweets='59', likes='423')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
