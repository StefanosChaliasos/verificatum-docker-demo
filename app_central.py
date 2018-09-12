from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse
from utils.commands import vmnc_pk, vmn_setpk, vmnc_ciphs, vmn_shuffle, \
        vmni_merge
import xmltodict
import json
import dicttoxml
import requests
import subprocess
import os
import sh


def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


app = Flask(__name__)
api = Api(app)
api.representations['application/xml'] = output_xml

parser = reqparse.RequestParser()

counter = 2
mixers = os.getenv('MIX_SERVERS_ORIGINS').split(',')


def leading_zero(x):
    if len(str(x)) <= 1:
        return '0' + str(x)
    return str(x)


class Params(Resource):
    def get(self):
        with open('/data/params.json') as f:
            params = json.load(f)
        return params


class InfoFile(Resource):
    def post(self):
        global counter
        data = request.data
        with open('/verificatum/protInfo' + leading_zero(counter) +
                  '.xml', 'w') as f:
            f.write(data)
        if counter == 3:
            print 15 * "*" + "ADMIN MESSAGE" + 15 * "*"
            print '*   We should inform the administrator   *'
            print 15 * "*" + "ADMIN MESSAGE" + 15 * "*"
        counter = counter + 1
        return 'Ok', 201


class Start(Resource):
    def get(self):
        # Run local scripts to initialize local mix server
        p = vmni_merge()
        p.wait()
        sh.cd('/verificatum')
        vmnc_pk()
        vmn_setpk()
        vmnc_ciphs()
        for mixer in mixers:
            # Post proInfoFiles
            for c in xrange(1, 4):  # counter here is 4
                with open('/verificatum/protInfo' + leading_zero(c) +
                          '.xml', 'r') as f:
                    data = f.read().replace('\n', '')
                    o = xmltodict.parse(data)
                    xml_data = dicttoxml.dicttoxml(o, attr_type=False,
                                                   root=False)
                    headers = {'Content-Type': 'application/xml'}
                    r = requests.post('http://' + mixer + '/api/info-file',
                                      data=xml_data, headers=headers)
            with open('/data/pkjson', 'r') as f:
                data = json.load(f)
                r = requests.post('http://' + mixer + '/api/pk', json=data)
            with open('/data/ciphertexts.json', 'r') as f:
                data = json.load(f)
                r = requests.post('http://' + mixer + '/api/ciphers',
                                  json=data)
            r = requests.get('http://' + mixer + '/api/setup')
            r = requests.get('http://' + mixer + '/api/begin')
        sh.cd('/verificatum')
        vmn_shuffle()
        return 'Mixnet starts'


api.add_resource(Params, '/api/params')
api.add_resource(InfoFile, '/api/info-file')
api.add_resource(Start, '/api/start')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
