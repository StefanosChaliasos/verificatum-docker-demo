import requests
import sys
import sh
import json

central_node = sys.argv[1]
central_node_ip = sys.argv[2]
ip = sys.argv[3]
portA = sys.argv[4]
portB = sys.argv[5]
hostname = sys.argv[6]
ms_name = sys.argv[7]  # mix server name

if central_node == "true":
    with open('/params.json') as f:
        params = json.load(f)
else:
    params = requests.get('http://' + central_node_ip + '/api/params').json()

modulus = params['pgroup']['modulus']
generator = params['pgroup']['generator']
order = params['pgroup']['order']
sid = params['sid']
name = params['name']
nopart = params['nopart']
thres = params['thres']

# Create zeus group
with open("/verificatum/zeus_group", "w") as h:
    sh.vog('-gen', 'ModPGroup', '-explic', modulus, generator, order, _out=h)

# Initialize mix server
with open("/verificatum/zeus_group", "r") as f:
    key = f.read().replace('\n', '')
sh.cd('/verificatum')
sh.vmni('-prot', '-sid', sid, '-name', name,
        '-nopart', nopart, '-thres', thres, '-pgroup', key)
sh.vmni('-party', '-name', 'Mix server ' + ms_name,
        '-httpl', 'http://' + hostname + ':' + portA,
        '-hintl', hostname + ':' + portB,
        '-http', 'http://' + ip + ':' + portA,
        '-hint', ip + ':' + portB)
