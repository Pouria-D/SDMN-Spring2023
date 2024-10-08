"""
In the name of god
SDMN HW1
Pouria Dadkhah - 401201381


Q3:

in this question we set the initial matix in the below format and calculate the best forward and backward flow for 1 to n
the in creat_flow itterate over both path and create corresponds xmls. except of begin and end that should handle mac
other switches are just in a path and have port flows.
at the end by itterating both path add created xmls on restconf

after running this file, we should delete preivouse flows and run creat_flows.py and then push_flows.py in mininet shell

the results are attached in screenshot

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
    ip="192.168.1.100",  # static ip defined in vm
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
