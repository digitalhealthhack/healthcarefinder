import json
import random
from flask import Flask
from flask.ext.restful import Api
from flask.ext.restful import Resource


APP = Flask(__name__)
API = Api(APP)


class HealthCenters(Resource):
    def get(self, latitude, longitude):
        with open('merged.json') as json_file:
            health_centers = []
            data = json.loads(json_file.read())
            for datum in data:
                health_centers.append({
                    datum['hospital']: {
                        'latitude': datum['lat'],
                        'longitude': datum['lng'],
                        'address': datum['address'],
                        'estimated': random.randint(90, 900)
                    }
                })

        return health_centers


API.add_resource(HealthCenters, '/<string:latitude>/<string:longitude>')


if __name__ == '__main__':
    APP.run(debug=True)

