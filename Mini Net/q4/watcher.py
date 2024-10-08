import time

import requests
from xml.etree import ElementTree
from dijkstraPath import calculatePath
import json
from os import system as cli
from create_flows import create_backward_flows
from create_flows import create_forward_flows
from push_flows import push_forward_flows
from push_flows import push_backward_flows
from push_flows import delete_forward_flows
from push_flows import delete_backward_flows

cli('python creat_flows.py')

topo = json.load(open('topo.txt'))
n = topo.__len__()
pathForward = calculatePath(initialGraph=topo, source='1', dest=f'{n}')
pathForwardLen = pathForward.__len__()

pathBackward = calculatePath(initialGraph=topo, source=f'{n}', dest='1')
pathBackwardLen = pathBackward.__len__()

topo = {
        '1': {'2': 10, '3': 3, '4': 4},
        '2': {'1': 2, '4': 1},
        '3': {'1': 3},
        '4': {'1': 1, '2': 1}
    }

requests.packages.urllib3.disable_warnings()

HOST = "192.168.1.100"
PORT = "8181"
USER = "admin"
PASSWORD = "admin"
header = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}


def updateTopo(liveStatus):
    live = {}
    for src in list(topo.keys()):
        keys = list(topo[src].keys())
        valuse = list(topo[src].values())
        live.update({src: dict(zip(keys, valuse))})

    for src in list(topo.keys()):
        for dst in list(topo[src].keys()):
            if liveStatus[src][dst] == 0:
                del live[src][dst]

    json.dump(live, open("liveTopo.txt", 'w'))
    return live


def checkLink(src, dst):
    
    node_id = f"openflow:{int(src)}"
    nodeConnector_id = f"{node_id}:{int(dst)}"
    # typical URL: “http://192.168.1.100:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:2/node-connector/openflow:2:4/flow-node-inventory:state”
    url = f"http://{HOST}:{PORT}/restconf/operational/opendaylight-inventory:nodes/node/{node_id}/node-connector/{nodeConnector_id}/flow-node-inventory:state"
    response = requests.get(url=url, headers=header, auth=(USER, PASSWORD))
    tree = ElementTree.fromstring(response.content)
    # checking link-down sub element value of each link
    for child in tree.iter('{urn:opendaylight:flow:inventory}link-down'):
        if child.text == 'true':
            print(f"link failure in {nodeConnector_id}")
            return False
        else:
            return True

status = {}
for src in list(topo.keys()):
    keys = list(topo[src].keys())
    valuse = list(topo[src].values())
    status.update({src: dict(zip(keys,valuse))})

for src in list(topo.keys()):
    for dst in list(topo[src].keys()):
        status[src][dst] = 1

print("initial status is:")
print(status)
while True:
    print('checking all links ...')
    flag = 0

    liveStatus = {}
    for src in list(topo.keys()):
        keys = list(topo[src].keys())
        valuse = list(topo[src].values())
        liveStatus.update({src: dict(zip(keys, valuse))})

    for src in topo:
        for dst in topo[src].keys():
            linkStatus = checkLink(src, dst)
            if linkStatus:
                liveStatus[src][dst] = 1
            else:
                liveStatus[src][dst] = 0
                flag = 1

    print("live status is:")
    print(liveStatus)
    print("begin of loop status is:")
    print(status)

    if flag == 0:
        print("All Links are OK.")

    if liveStatus == status:
        print("Same network topology ...")
    else:
        liveTopo = updateTopo(liveStatus)
        print("Calculating new path ...")
        newPathForward = calculatePath(initialGraph=liveTopo, source='1', dest=f'{n}')
        newPathBackward = calculatePath(initialGraph=liveTopo, source=f'{n}', dest='1')

        if newPathForward != pathForward:
            # ToDo call create_flows and push_flows and then set new path to path
            # cli('python create_net.py')
            # create new forward flows and push them to network
            create_forward_flows()
            delete_forward_flows()
            push_forward_flows()
            print(newPathForward)
            print("new forward flows has been added")

        if newPathBackward != pathBackward:
            create_backward_flows()
            delete_backward_flows()
            push_backward_flows()
            print("new backward flows has been added")
        if newPathBackward == pathBackward and newPathForward == pathForward:
            print("current path is OK.")

        pathForward = newPathForward
        pathBackward = newPathBackward

    status = {}
    for src in list(liveStatus.keys()):
        keys = list(liveStatus[src].keys())
        valuse = list(liveStatus[src].values())
        status.update({src: dict(zip(keys, valuse))})

    time.sleep(5)

