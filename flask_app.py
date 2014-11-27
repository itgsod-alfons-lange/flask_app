from flask import Flask, render_template

from lib.fakultet import fakultet

import datetime

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('hello.html',title="hackerspace")

@app.route('/user/<username>')
def hello_user(username):
    return render_template('user.html', username=username, title="hackerspace")

@app.route('/getdata/<place>')
def get_data(place):
    import json, urllib

    json_place = urllib.urlopen("http://alfonslange.se/sl/times/getTimes.php?siteid=%s&timewindow=60" % place)

    response = json.loads(json_place.read())['ResponseData']

    for i in range(len(response['Trains'])):
        scheduled_time = response['Trains'][i]['TimeTabledDateTime']
        d_schedule = datetime.datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%S")

        expected_time = response['Trains'][i]['ExpectedDateTime']
        d_expect = datetime.datetime.strptime(expected_time, "%Y-%m-%dT%H:%M:%S")

        time_late = "(" + str((d_expect-d_schedule).seconds/60) + "min)" if ((d_expect-d_schedule).seconds/60 != 0) else ""
        response['Trains'][i]['Late'] = time_late

    for i in range(len(response['Buses'])):
        scheduled_time = response['Buses'][i]['TimeTabledDateTime']
        d_schedule = datetime.datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%S")

        expected_time = response['Buses'][i]['ExpectedDateTime']
        d_expect = datetime.datetime.strptime(expected_time, "%Y-%m-%dT%H:%M:%S")

        time_late = "(" + str((d_expect-d_schedule).seconds/60) + "min)" if ((d_expect-d_schedule).seconds/60 != 0) else ""
        response['Buses'][i]['Late'] = time_late

    return render_template('getdata.html', data=response, title="JSON-test")


@app.route('/fakultet/<tal>')
def count_fakultet(tal):

    res = fakultet(int(tal))

    return str(res)

if __name__ == '__main__':
    app.run(debug=True, port=80)
