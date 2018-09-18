from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import os


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


mixers = []


class Params(Resource):
    def get(self):
        with open('/data/params.json') as f:
            params = json.load(f)
        params['mix-servers'] = mixers
        return params


class MixServerUrl(Resource):
    def post(self):
        global mixers
        data = json.loads(request.data)
        mixers.append(data['protInfoUrl'])
        print(mixers)
        return 'Ok', 201


api.add_resource(Params, '/api/params')
api.add_resource(MixServerUrl, '/api/address')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
