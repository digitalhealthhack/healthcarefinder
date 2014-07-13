import json
import random
import math

import requests
from flask import Flask
from flask import Response
from flask import render_template
from flask.ext.restful import Api
from flask.ext.restful import Resource


APP = Flask(__name__)

API = Api(APP)


def get_longitude_and_latitude_from_postcode(postcode):
    #url = 'http://api.geonames.org/findNearbyPostalCodesJSON'
    #query_args = {
    #    'postalcode': postcode,
    #    'country': 'GB',
    #    'radius': 10,
    #    'username': 'demo',
    #}
    #response = requests.get(url, params=query_args)
    #postal_codes = response.json().get('postalCodes')
    #if not postal_codes:
    #    return None
    with open('findNearbyPostalCodesJSON.json') as mock_file:
        postal_codes = json.loads(mock_file.read()).get('postalCodes')

    first_postal_code = postal_codes[0]
    return first_postal_code['lat'], first_postal_code['lng']


# Taken from http://www.johndcook.com/python_longitude_latitude.html
def distance_on_unit_sphere(lat1, lat2, long1, long2):
    degrees_to_radians = math.pi/180.0

    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
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
        if distance < 0.005:
            filtered_data.append(datum)
    return filtered_data


class HealthCenters(Resource):
    def get(self, postcode):
        lat, lng = get_longitude_and_latitude_from_postcode(postcode)
        with open('data.json') as json_file:
            health_centers = []
            data = json.loads(json_file.read())
            filtered_data = get_data_filtered(data, lat, lng)
            for datum in filtered_data:
                health_centers.append({
                    'name': datum['hospital'],
                    'lat': datum['lat'],
                    'long': datum['lng'],
                    'address': datum['address'],
                    'estimated': random.randint(90, 900)
                })

        return Response(json.dumps(health_centers),  mimetype='application/javascript')

API.add_resource(HealthCenters, '/<string:postcode>')

@APP.route("/")
def map():
    return render_template('index.html')

if __name__ == '__main__':
    APP.run(debug=True)

