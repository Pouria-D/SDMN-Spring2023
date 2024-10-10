"""
In the name of god
SDMN HW1
Pouria Dadkhah - 401201381


Q2. Part1:

in this question we build network by proper link adding and then installed odl used its dlux and yang ui and other parts to see the details of flows
the controller added porperl flows its self by l2switch and hosts can ping each other

the results are attached in screenshot

"""
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import math

setLogLevel( 'info' )

net = Mininet(controller=RemoteController,
              switch=OVSKernelSwitch,
              link=TCLink
              )

# Adding hosts
h = []
for i in range(1, 9):
    hostName = "h" + str(i)
    h.append(net.addHost(
        name=hostName,
        ip="10.0.0."+str(i),
        mac="00:00:00:00:00:0"+str(i),
        defaultRoute="h"+str(i)+"-eth0"
    ))

# Adding switches
s = []
for i in range(1, 8):
    s.append( net.addSwitch(
        name="s"+str(i)
    ))

# Adding controller (if any!)
c0 = net.addController(
    name="c0",
    ip="192.168.1.100",  # static ip defined in vm
    port=6633,
    protocols="OpenFlow13"
)

# Adding links
for i in range(1, 9):
    s_index = math.ceil(i/2)
    s_port = 2 - (i % 2)
    net.addLink(h[i-1], s[s_index-1], 0, s_port)

for i in range(1, 5):
    s_index = 4 + math.ceil(i / 2)
    s_port = 2 - (i % 2)
    net.addLink(s[i-1], s[s_index-1], 3, s_port)

net.addLink(s[4], s[6], 3, 1)
net.addLink(s[5], s[6], 3, 2)

# Start controller on switches (if any!)
c0.start()
for i in range(0,7):
    s[i].start([c0])

# Start CLI and build the network

net.build()
net.start()
CLI(net)
net.stop()

