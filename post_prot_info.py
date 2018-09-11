import xmltodict, dicttoxml, requests
import sys

central = sys.argv[1]

with open('/verificatum/localProtInfo.xml', 'r') as f:
    data = f.read().replace('\n', '')
    o = xmltodict.parse(data)
    xml = dicttoxml.dicttoxml(o, attr_type=False, root=False)
    headers = {'Content-Type': 'application/xml'}
    r = requests.post('http://' + central + '/api/info-file', data=xml,
                      headers=headers)
    print('OOOOO')
    print(r.status_code)
    print('OOOOO')
