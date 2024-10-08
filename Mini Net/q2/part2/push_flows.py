import requests

flows = ['Switch1-OutputFlow', 'Switch1-InputFlow', 'Switch1-ArpFlow',
         'Switch2-InputFlow', 'Switch2-OutputFlow', 'Switch2-ArpFlow',
         'Router-IP1Flow', 'Router-IP2Flow']

requests.packages.urllib3.disable_warnings()

HOST = "192.168.1.100"
PORT = "8181"
USER = "admin"
PASSWORD = "admin"
header = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}

# add flows for s1,s2 and s3:
counter = 0
for i in range(1, 4):
    switch_id = i
    node_id = f"openflow:{switch_id}"
    table_id = 0
    # add simple switch (port and mac) flows for each s1 and s2 and routing flows (arp and ip packet handling) for s3
    for j in range(1, 4):
        # s1,s2 has only 3 flows but s3 has 4
        if j == 3 and i == 3:
            break
        flow_id = j
        # typical file name: openflow:1-flow1
        fileLocation = f'./Flows/{flows[counter]}.xml'
        xmlFile = open(fileLocation, 'rb')
        # typical URL: “http://<controller IP>:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1”
        url = f"http://{HOST}:{PORT}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
        response = requests.put(url=url, data=xmlFile, headers=header, auth=(USER, PASSWORD))
        print(f"Switch: {switch_id}, flow: {flow_id}    {response.status_code}")
        counter += 1
