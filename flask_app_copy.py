from flask import Flask, render_template

from lib.fakultet import fakultet

import datetime

app = Flask(__name__)

def return_time_diff(scheduled, expected):
    d_schedule = datetime.datetime.strptime(expected, "%Y-%m-%dT%H:%M:%S")
    d_schedule = d_schedule.replace(second=0)

    d_expect = datetime.datetime.strptime(scheduled, "%Y-%m-%dT%H:%M:%S")
    d_expect = d_expect.replace(second=0)

    if d_expect < d_schedule:
        temp = d_schedule
        d_schedule = d_expect
        d_expect = temp
    time_late = "(" + str((d_expect-d_schedule).seconds/60) + " min)" if ((d_expect-d_schedule).seconds/60 != 0) else ""
    return time_late


@app.route('/')
def welcome():
    return render_template('hello.html',title="hackerspace")

@app.route('/user/<username>')
def hello_user(username):
    return render_template('user.html', username=username, title="hackerspace")

@app.route('/getdata/<place>')
def get_data(place):
    import json, urllib, config, requests

    siteid = "7006"

    url = "http://api.sl.se/api2/realtimedepartures.json?key={apikey}&siteid={siteid}&timewindow={timewindow}"

    url = url.format(apikey=config.apikey,siteid=siteid,timewindow=60)

    json_res = requests.get(url)

    response = json_res.json()['ResponseData']

    for i in range(len(response['Trains'])):

        scheduled_time = response['Trains'][i]['TimeTabledDateTime']
        expected_time = response['Trains'][i]['ExpectedDateTime']

        time_late = return_time_diff(scheduled_time,expected_time)

        response['Trains'][i]['Late'] = time_late

    for i in range(len(response['Buses'])):
        scheduled_time = response['Buses'][i]['TimeTabledDateTime']
        expected_time = response['Buses'][i]['ExpectedDateTime']

        time_late = return_time_diff(scheduled_time,expected_time)

        response['Buses'][i]['Late'] = time_late

    return render_template('getdata.html', data=response, title="JSON-test")


@app.route('/fakultet/<tal>')
def count_fakultet(tal):

    res = fakultet(int(tal))

    return str(res)

if __name__ == '__main__':
    app.run(debug=True, port=80)
