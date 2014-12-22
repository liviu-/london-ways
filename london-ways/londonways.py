import os
import json
import requests

import redis

from flask import Flask, render_template, request

app = Flask(__name__)
conn = redis.Redis('localhost')

PORT = 5000

# Constants because the data doesn't get updated
# dynamically and it's required in a bunch of places
KEYS = conn.keys()
VALUES = conn.mget(KEYS)
STATIONS = list(zip([key.decode('utf-8') for key in KEYS],
                    [bstation.decode('utf-8').title() for bstation
                     in VALUES]))


@app.route("/")
def index():
    return render_template('index.html', stations=STATIONS)


@app.route("/<int:bus_id>")
def get_bus(bus_id):
    buses = get_info(bus_id, is_ajax=False)
    station = conn.get(bus_id).decode('utf-8').title()
    return render_template('bus_station.html', buses=buses, bus_id=bus_id,
                           station=station, stations=STATIONS)


@app.route("/data/json")
def get_info(bus_id=None, is_ajax=True):
    bus_id = bus_id or request.args.get('bus_id')
    try:
        json_dict = requests.get("http://countdown.tfl.gov.uk/stopBoard/"
                                 "{bus_id}".format(bus_id=bus_id)).json()
    except ValueError:
        return render_template('bus_station.html',
                               station="Station not found",
                               stations=STATIONS)

    data = json_dict['arrivals']
    bus_data = [(bus['routeId'], bus['destination'], bus['estimatedWait'])
                for bus in data if bus['isRealTime'] and not bus['isCancelled']]

    if is_ajax:
        return json.dumps(bus_data)
    return bus_data


if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get('PORT', PORT))
    app.run(host='0.0.0.0', port=port)
