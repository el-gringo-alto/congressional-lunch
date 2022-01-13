from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', description='test description')

@app.route('/about')
def about():
    return render_template('about.html', title='About', retweets='59', likes='423')

@app.route('/test')
def test():
    return render_template('single.html', title='About', retweets='59', likes='423')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
