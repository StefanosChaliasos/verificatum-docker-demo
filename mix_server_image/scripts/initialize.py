import requests
import sys
import sh
import json
import time

server = sys.argv[1]
ip = sys.argv[2]
port = sys.argv[3]
portA = sys.argv[4]
portB = sys.argv[5]
hostname = sys.argv[6]
ms_name = sys.argv[7]  # mix server name


def leading_zero(x):
    if len(str(x)) <= 1:
        return '0' + str(x)
    return str(x)


params = None
print "Initialize params"
while not params:
    params_url = 'http://' + server + '/api/params'
    print "Resolve params from ", params_url
    try:
        params = requests.get(params_url).json()
    except Exception as e:
        print "Cannot resolve params", e
        pass
    if not params:
        time.sleep(3)

modulus = params['group']['modulus']
generator = params['group']['generator']
order = params['group']['order']
sid = params['verificatum']['sid']
name = params['verificatum']['name']
nopart = params['verificatum']['nopart']
thres = params['verificatum']['thres']

# Create zeus group
with open("/verificatum/zeus_group", "w") as h:
    sh.cd('/verificatum')
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

# Copy localProtInfo to exposed folder
sh.cp('/verificatum/localProtInfo.xml', '/data/localProtInfo.xml')

# Send address to server
address = {'protInfoUrl': ip + ':' + port}
headers = {'Content-Type': 'application/json'}
r = requests.post('http://' + server + '/api/address', json=address,
                  headers=headers)

# Get the addresses of others mix-servers
mixers = []
while len(mixers) != int(nopart):
    params_url = 'http://' + server + '/api/params'
    print "Resolve params (mixers) from ", params_url
    try:
        mixers_result = requests.get(params_url).json()
        mixers = mixers_result['mix-servers']
    except Exception as e:
        print "Cannot resolve params", e
        pass
    if len(mixers) != nopart:
        time.sleep(3)

print(mixers)

# Get and save prot info files
for i, mix_server in enumerate(mixers):
    r = requests.get('http://' + mix_server + '/localProtInfo.xml')
    with open('/verificatum/protInfo' + leading_zero(i+1) + '.xml', 'w') as f:
        f.write(r.content)

print(sh.ls('/verificatum'))
