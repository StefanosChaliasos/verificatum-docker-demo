from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse
import xmltodict, json, dicttoxml, requests
import subprocess
import os


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
        with open('/params.json') as f:
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
            print 'We should inform the administrator'
        counter = counter + 1
        return 'Ok', 201


class Start(Resource):
    def get(self):
        # Run local scripts to initialize local mix server
        process = subprocess.Popen('/verificatum/create_prot_info.sh',
                                   shell=True, stdout=subprocess.PIPE)
        process.wait()
        process_pk = subprocess.Popen('/verificatum/set_pk.sh',
                                      shell=True)
        process_ciphs = subprocess.Popen('/verificatum/set_ciphertexts.sh',
                                         shell=True)
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
            with open('/verificatum/pkjson', 'r') as f:
                data = json.load(f)
                r = requests.post('http://' + mixer + '/api/pk', json=data)
            with open('/verificatum/ciphertexts.json', 'r') as f:
                data = json.load(f)
                r = requests.post('http://' + mixer + '/api/ciphers',
                                  json=data)
            r = requests.get('http://' + mixer + '/api/setup')
            r = requests.get('http://' + mixer + '/api/begin')
        process = subprocess.Popen('/verificatum/run.sh',
                                   shell=True)
        return 'Mixnet starts'


api.add_resource(Params, '/api/params')
api.add_resource(InfoFile, '/api/info-file')
api.add_resource(Start, '/api/start')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
