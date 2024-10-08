"""
In the name of god
SDMN HW1
Pouria Dadkhah - 401201381


Q1. Part1:

in this question both hosts are in the same subnets and they can achieve their mac
so it's just enough to add first layer flows fo switchies to rout all flows from one host to another
in other way for in_port = 1 it should send from port2 and otherwise.

we build the network from the sample code in question and just add hosts switches and links as requested with no controller

at the end delete preivouse flows on switches and run proper commands in mininet shell to add mentioned flows:
for example:
sh ovs-ofctl add-flow s1 in_port=1,actions=output:2
the results are attached in screenshot

"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from os import system as terminal

setLogLevel( 'info' )

net = Mininet(controller=None,  # None if we don't want any controller
              # RemoteController if you are using an
              # external SDN controller (like ODL)
              switch=OVSKernelSwitch,
              link=TCLink
              )

# Adding hosts

h1 = net.addHost(
    name="h1",
    ip="10.0.0.1/24"
)
h2 = net.addHost(
    name="h2",
    ip="10.0.0.2/24"
)

# Adding switches
s1 = net.addSwitch(
    name="s1"
)
s2 = net.addSwitch(
    name="s2"
)

# Adding links
net.addLink(h1, s1)
net.addLink(h2, s2)
net.addLink(s1, s2)

# Start CLI and build the network

net.build()
net.start()

terminal('ovs-ofctl del-flows s1')
terminal('ovs-ofctl del-flows s1')

CLI(net)
net.stop()

