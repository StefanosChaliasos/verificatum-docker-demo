import requests
import sys
from utils.util import serve_protinfo, get_params, create_group,\
        init_mix_server, save_prot_info_files, create_pk, merge_prot_files, \
        create_ciphertexts, run_mix_server


folder = '/verificatum'
group_name = 'zeus_group'

server_url = sys.argv[1]
ip = sys.argv[2]
port = int(sys.argv[3])
portA = sys.argv[4]
portB = sys.argv[5]
hostname = sys.argv[6]
ms_name = sys.argv[7]  # mix server name

# Get params from server
params = get_params(server_url)

crypto = params['group']
vrf_params = params['verificatum']

# Create zeus group
create_group(folder, group_name, crypto)

# Initialize mix server
init_mix_server(folder, group_name, hostname, portA, portB, ip, vrf_params,
                ms_name)

# Send address to server
address = {'protInfoUrl': ip + ':' + str(port)}
headers = {'Content-Type': 'application/json'}
r = requests.post('http://' + server_url, json=address, headers=headers)

# Read protInfoFile and create server
with open(folder + '/localProtInfo.xml', 'r') as f:
    local_prot_info = f.read()
server = serve_protinfo(local_prot_info, port)  # local server process

# save prot info files to folder
ip_port = ip + ':' + str(port)
save_prot_info_files(vrf_params['nopart'], server_url, folder, ip_port)

# Merge prot info files
merge_prot_files(folder)

# Create public key file
create_pk(folder, params['publicKey'])

# Create ciphertexts file
create_ciphertexts(folder, params['ciphertexts'])

# Run the mix server
run_mix_server(folder)
