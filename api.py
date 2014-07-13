import os
import json
import random
import math

import requests
from flask import Flask
from flask import Response
from flask import render_template
from flask.ext.restful import Api
from flask.ext.restful import Resource


COLOUR_RED = '#FF003C'
COLOUR_YELLOW = '#FABE28'
COLOUR_GREEN = '#88C100'

APP = Flask(__name__)

API = Api(APP)


def get_longitude_and_latitude_from_postcode(postcode):
    url = 'http://api.geonames.org/findNearbyPostalCodesJSON'
    postal_code_api_username = os.environ.get('POSTCODE_USERNAME') or 'demo'
    if postal_code_api_username == 'demo':
        print "USING DEMO USERNAME"
    query_args = {
        'postalcode': postcode,
        'country': 'GB',
        'radius': 10,
        'username': postal_code_api_username,
    }
    response = requests.get(url, params=query_args)
    postal_codes = response.json().get('postalCodes')
    if not postal_codes:
        with open('findNearbyPostalCodesJSON.json') as mock_file:
            postal_codes = json.loads(mock_file.read()).get('postalCodes')

    first_postal_code = postal_codes[0]
    return first_postal_code['lat'], first_postal_code['lng']


# Taken from http://www.johndcook.com/python_longitude_latitude.html
def distance_on_unit_sphere(lat1, lat2, long1, long2):
    degrees_to_radians = math.pi/180.0

    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    cos = (
        math.sin(phi1) * math.sin(phi2) *
        math.cos(theta1 - theta2) +
        math.cos(phi1) * math.cos(phi2)
    )
    arc = math.acos(cos)
    return arc


def get_data_filtered(data, lat, lng):
    filtered_data = []
    for datum in data:
        distance = distance_on_unit_sphere(
            lat,
            float(datum['lat']),
            lng,
            float(datum['lng']),
        )
        if distance < 0.003:
            filtered_data.append(datum)
    return filtered_data


def self_location(postcode, lat, lng):
    location = {
        'name': 'You',
        'address': postcode,
        'lat': lat,
        'long': lng,
        'hexcolor': '#FFFFFF'
    }
    return location


class HealthCenters(Resource):
    def get(self, postcode):
        with open('data.json') as json_file:
            data = json.loads(json_file.read())

        health_centers = []
        lat, lng = get_longitude_and_latitude_from_postcode(postcode)
        health_centers.append(self_location(postcode, lat, lng))

        filtered_data = get_data_filtered(data, lat, lng)
        for datum in filtered_data:
            estimate = random.randint(90, 400)
            if estimate > 200:
                hexcolor = COLOUR_RED
            elif estimate > 100:
                hexcolor = COLOUR_YELLOW
            else:
                hexcolor = COLOUR_GREEN
            health_centers.append({
                'name': datum['hospital'],
                'lat': datum['lat'],
                'long': datum['lng'],
                'address': datum['address'],
                'estimated': estimate,
                'hexcolor': hexcolor,
            })

        return Response(json.dumps(health_centers),  mimetype='application/javascript')

API.add_resource(HealthCenters, '/api/<string:postcode>')

@APP.route("/<string:postcode>")
def map(postcode):
    return render_template('index.html', postcode=postcode)

if __name__ == '__main__':
    APP.run(debug=True)

