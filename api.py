import json
import random
from flask import Flask, Response
from flask.ext.restful import Api
from flask.ext.restful import Resource

APP = Flask(__name__)
API = Api(APP)

class HealthCenters(Resource):
    def get(self, latitude, longitude):
        with open('data.json') as json_file:
            health_centers = []
            data = json.loads(json_file.read())
            for datum in data:
                health_centers.append({
                    'name': datum['hospital'],
                    'lat': datum['lat'],
                    'long': datum['lng'],
                    'address': datum['address'],
                    'estimated': random.randint(90, 900)
                    
                })

        return Response(json.dumps(health_centers),  mimetype='application/javascript')

API.add_resource(HealthCenters, '/<string:latitude>/<string:longitude>')

if __name__ == '__main__':
    APP.run(debug=True)

