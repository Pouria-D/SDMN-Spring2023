"""
In the name of god
SDMN HW1
Pouria Dadkhah - 401201381

Q4
In this question, we also use the codes from the previous section. In this way, we check a condition (creating an effective change on the network links) in a certain period of time, and if it is fulfilled, we find the new optimal route according to the new situation and resend it to the switches. The following considerations apply:
- The review period is 30 seconds
- The initial value of the matrices and the state of the network and the optimal path and the sent flows are according to the original matrix (the initial matrix and here the example matrix in case of question) and can have any other initial value
- From the initial matrix, a connection status matrix is created, which shows whether each link is disconnected or connected. This matrix is obtained by traversing the links of the original matrix one by one and querying RESTCONF.
- In every period of 30 seconds, the state of the connection state matrix is compared with the same matrix in the previous round, and if no changes have been made, no new flow is sent.
- In case of inequality of two matrices, the fields must be corrected.
- The correction is done in this way that a new matrix is made from the original matrix and by querying the broken links, which shows the remaining links with zero interruptions and with the value of the cost weight of the remaining links.
- Next, this new matrix is given to Jikanshara as in question 3, and if the new optimal path is different from the previous one, new flows are created and sent based on the new matrix.
- It should be noted that when comparing the previous route and the new proposed route, it is possible to separate the flows of the round trip route on the route between the two hosts. In this case, only one of the two modes may have changed and additional changes are not applied to the other mode, which makes the code optimal.
"""
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from dijkstraPath import calculatePath
import json

setLogLevel('info')

def initial_graph():

    topo = {
        '1': {'2': 2, '3': 3, '4': 4},
        '2': {'1': 2, '4': 1},
        '3': {'1': 3},
        '4': {'1': 1, '2': 1}
    }
    json.dump(topo, open("topo.txt", 'w'))
    json.dump(topo, open("liveTopo.txt", 'w'))
    return topo

# input graph:
topo = initial_graph()
n = topo.__len__()


net = Mininet(controller=RemoteController,
              switch=OVSKernelSwitch,
              link=TCLink
              )

# Adding hosts

h1 = net.addHost(
    name="h1",
    ip="10.0.1.1/24",
    mac="00:00:00:00:00:01",
    defaultRoute="h1-eth0"
)
h2 = net.addHost(
    name="h2",
    ip="10.0.2.1/24",
    mac="00:00:00:00:00:02",
    defaultRoute="h2-eth0"
)

# Adding switches
s = []
for i in range(1, n+1):
    s.append(
        net.addSwitch(
            name=f"s{i}"
        )
    )

# Adding controller (if any!)
c0 = net.addController(
    name="c0",
    ip="127.0.0.1",
    port=6633
)

# Adding links
net.addLink(h1, s[0], 0, n+1)
net.addLink(h2, s[n-1], 0, n+1)
for src in topo:
    for dst in topo[src].keys():
        s_port1 = int(dst)
        s_port2 = int(src)
        if src < dst:
            net.addLink(s[int(src)-1], s[int(dst)-1], s_port1, s_port2)

c0.start()
for i in range(0, n):
    s[i].start([c0])

# Start CLI and build the network

net.build()
net.start()

h1.cmd("arp -s 10.0.2.1 00:00:00:00:00:04")
h2.cmd("arp -s 10.0.1.1 00:00:00:00:00:03")

CLI(net)
net.stop()

