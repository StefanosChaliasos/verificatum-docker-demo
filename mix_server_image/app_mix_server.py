from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from utils.commands import vmnc_pk, vmn_setpk, vmnc_ciphs, vmn_shuffle, \
        vmni_merge
import json
import subprocess
import os
import sh


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

counter = 1


def leading_zero(x):
    if len(str(x)) <= 1:
        return '0' + str(x)
    return str(x)


class PublicKey(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        with open('/data/pkjson', 'w') as f:
            json.dump(json_data, f, separators=(',', ':'))
        return 'Public key saved', 201


class CipherTexts(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        with open('/data/ciphertextsjson', 'w') as f:
            for c in json_data:
                json.dump(c, f, separators=(',', ':'))
                f.write('\n')
        return 'Ciphertexts saved', 201


class InfoFile(Resource):
    def post(self):
        global counter
        data = request.data
        with open('/verificatum/protInfo' + leading_zero(counter) +
                  '.xml', 'w') as f:
            f.write(data)
        counter = counter + 1
        return data, 201


class SetUp(Resource):
    def get(self):
        p = vmni_merge()
        p.wait()
        sh.cd('/verificatum')
        vmnc_pk()
        vmn_setpk()
        vmnc_ciphs()
        # run local scripts
        return 'Mix server setup up completed'


class Begin(Resource):
    def get(self):
        vmn_shuffle()
        return 'Mix server begins'


api.add_resource(PublicKey, '/api/pk')
api.add_resource(InfoFile, '/api/info-file')
api.add_resource(SetUp, '/api/setup')
api.add_resource(CipherTexts, '/api/ciphers')
api.add_resource(Begin, '/api/begin')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
