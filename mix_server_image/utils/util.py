from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing import Process
from .commands import vmnc_pk, vmni_merge, vmnc_ciphs, vmn_shuffle, vmn_setpk
import json
import requests
import time
import sh
import os
import posixpath
import urllib
from shutil import copyfile


def leading_zero(x):
    if len(str(x)) <= 1:
        return '0' + str(x)
    return str(x)


class RootedHTTPServer(HTTPServer):

    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path


class GetServer(BaseHTTPRequestHandler):
    get_data = None

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        self.wfile.write(self.get_data)

    @staticmethod
    def serve(data, port=8000, address='', **kwargs):
        bind = (address, port)

        class Handler(GetServer):
            get_data = data

        server = HTTPServer(bind, Handler)
        server.serve_forever()


def serve_protinfo(protinfo_data, port, address=''):
    process = Process(target=GetServer.serve, args=(protinfo_data, port,
                                                    address))
    process.start()
    return process


def get_params(url):
    params = None
    print "Initialize params"
    while not params:
        params_url = 'http://' + url
        print "Resolve params from ", params_url
        try:
            params = requests.get(params_url).json()
        except Exception as e:
            print "Cannot resolve params", e
            pass
        if not params:
            time.sleep(3)
    return params


def create_group(path, group_name, crypto):
    with open(path + '/' + group_name, 'w') as f:
        sh.cd(path)
        sh.vog('-gen', 'ModPGroup', '-explic', crypto['modulus'],
               crypto['generator'], crypto['order'], _out=f)


def init_mix_server(path, group_name, hostname, portA, portB, ip, vrf_params,
                    ms_name):
    sid = vrf_params['sid']
    name = vrf_params['name']
    nopart = vrf_params['nopart']
    thres = vrf_params['thres']
    with open(path + '/' + group_name, 'r') as f:
        key = f.read().replace('\n', '')
    sh.cd(path)
    sh.vmni('-prot', '-sid', sid, '-name', name,
            '-nopart', nopart, '-thres', thres, '-pgroup', key)
    sh.vmni('-party', '-name', 'Mix server ' + ms_name,
            '-httpl', 'http://' + hostname + ':' + portA,
            '-hintl', hostname + ':' + portB,
            '-http', 'http://' + ip + ':' + portA,
            '-hint', ip + ':' + portB)


def get_mix_servers(nopart, server_url):
    mix_servers = []
    while len(mix_servers) != int(nopart):
        params_url = 'http://' + server_url
        print "Resolve params (mixers) from ", params_url
        try:
            r = requests.get(params_url).json()
            mix_servers = r['mix-servers']
        except Exception as e:
            print "Cannot resolve params", e
            pass
        if len(mix_servers) != int(nopart):
            time.sleep(3)
    return mix_servers


def save_prot_info_files(nopart, server_url, path, ip_port):
    mix_servers = get_mix_servers(nopart, server_url)
    for mix_server in mix_servers:
        try:
            r = requests.get('http://' + mix_server)
            # FIXME
            with open(path + '/protInfo' + leading_zero(
                mix_server.split(":")[0][-1]) + '.xml',
                      'w') as f:
                f.write(r.content)
        except Exception as e:
            print "Cannot get localProtInfo", e
            pass


def merge_prot_files(path):
    vmni_merge(path)


def create_pk(path, pk):
    with open(path + '/pkjson', "w") as f:
        json.dump(pk, f, separators=(',', ':'))
    sh.cd(path)
    vmnc_pk(path)
    vmn_setpk()


def create_ciphertexts(path, ciphertexts):
    with open(path + '/ciphertextsjson', 'w') as f:
        for c in ciphertexts:
            json.dump(c, f, separators=(',', ':'))
            f.write('\n')
    vmnc_ciphs(path)


def run_mix_server(path):
    vmn_shuffle()


def serve_results(path, port, folder='/results'):
    os.makedirs(folder)
    vmnc_ciphs(path, 'ciphertexts', 'ciphertexts.json', ('raw', 'json'))
    copyfile(path + '/ciphertexts.json', folder + '/ciphertexts.json')
    copyfile(path + '/protInfo.xml', folder + '/protInfo.xml')
    sh.cp('-r', path + '/dir/nizkp/default/proofs/', folder)
    server_address = ('', port)
    httpd = RootedHTTPServer(folder, server_address, RootedHTTPRequestHandler)
    return httpd
