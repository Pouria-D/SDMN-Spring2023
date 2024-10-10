import requests
from dijkstraPath import calculatePath
import json

topo = json.load(open('topo.txt'))
n = topo.__len__()
pathForward = calculatePath(initialGraph=topo, source='1', dest=f'{n}')
pathForwardLen = pathForward.__len__()


pathBackward = calculatePath(initialGraph=topo, source=f'{n}', dest='1')
pathBackwardLen = pathBackward.__len__()


requests.packages.urllib3.disable_warnings()

HOST = "192.168.1.100"
PORT = "8181"
USER = "admin"
PASSWORD = "admin"
header = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}


#delete forward flows:
for i in range(0, pathForwardLen):
    switch_id = pathForward[i]
    node_id = f"openflow:{switch_id}"
    table_id = 0

    # typical URL: “http://<controller IP>:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0
    url = f"http://{HOST}:{PORT}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}"
    response = requests.delete(url=url, headers=header, auth=(USER, PASSWORD))
    print(f"Switch: {switch_id},delete previous flows  {response.status_code}")

# delete forward flows:
for i in range(0, pathBackwardLen):
    switch_id = pathBackward[i]
    node_id = f"openflow:{switch_id}"
    table_id = 0

    # typical URL: “http://<controller IP>:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0
    url = f"http://{HOST}:{PORT}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}"
    response = requests.delete(url=url, headers=header, auth=(USER, PASSWORD))
    if response.status_code == 200:
        print(f"Switch: {switch_id},delete previous flows  {response.status_code}")

# add forward flows:
for i in range(0, pathForwardLen):
    switch_id = pathForward[i]
    node_id = f"openflow:{switch_id}"
    table_id = 0
    flow_id = 1
    fileLocation = f'./Flows/switch-{switch_id}-forwardFlow.xml'

    xmlFile = open(fileLocation, 'rb')
    # typical URL: “http://<controller IP>:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1”
    url = f"http://{HOST}:{PORT}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
    response = requests.put(url=url, data=xmlFile, headers=header, auth=(USER, PASSWORD))
    print(f"Switch: {switch_id}, flow: {flow_id}    {response.status_code}")
# add backward flows
for i in range(0, pathBackwardLen):
    switch_id = pathBackward[i]
    node_id = f"openflow:{switch_id}"
    table_id = 0
    flow_id = 2

    fileLocation = f'./Flows/switch-{switch_id}-backwardFlow.xml'
    xmlFile = open(fileLocation, 'rb')
    # typical URL: “http://<controller IP>:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1”
    url = f"http://{HOST}:{PORT}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
    response = requests.put(url=url, data=xmlFile, headers=header, auth=(USER, PASSWORD))
    print(f"Switch: {switch_id}, flow: {flow_id}    {response.status_code}")