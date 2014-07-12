from flask import Flask
from flask.ext.restful import Api
from flask.ext.restful import Resource


APP = Flask(__name__)
API = Api(APP)


class HealthCenters(Resource):
    def get(self, latitude, longitude):
        return [
            {
                'health_center': {
                    'latitude': '1233',
                    'longitude': '123',
                    'estimated_wait': 123,
                },
            }
        ]


API.add_resource(HealthCenters, '/<string:latitude>/<string:longitude>')


if __name__ == '__main__':
    APP.run(debug=True)

