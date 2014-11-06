from flask import Flask, render_template

from lib.fakultet import fakultet

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('hello.html',title="hackerspace")

@app.route('/user/<username>')
def hello_user(username):
    return render_template('user.html', username=username, title="hackerspace")

@app.route('/fakultet/<tal>')
def count_fakultet(tal):

    res = fakultet(int(tal))

    return str(res)

if __name__ == '__main__':
    app.run(debug=True)
