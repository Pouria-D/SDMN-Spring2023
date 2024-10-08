"""
In the name of god
SDMN HW1
Pouria Dadkhah - 401201381


Q2. Part2:

in this part we turned off l2switch and added proper xml flows to controller api we python requests and created flows to handle the same
flows as q1 part1.
the typical xml files and url was driven from odl document and their match and actions has been set during creat_flows.py
they have been addes extra arp flow handler as same and not needed

after running this file, we should delete preivouse flows and run creat_flows.py and then push_flows.py in mininet shell

the results are attached in screenshot

"""
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

setLogLevel( 'info' )

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
s1 = net.addSwitch(
    name="s1"
)
sr = net.addSwitch(
    name="s3"
)
s2 = net.addSwitch(
    name="s2"
)

# Adding controller (if any!)
c0 = net.addController(
    name="c0",
    ip="192.168.1.100",  # static ip defined in vm
    port=6633,
    protocols="OpenFlow13"
)

# Adding links
net.addLink(h1, s1)
net.addLink(h2, s2)
net.addLink(s1, sr)
net.addLink(sr, s2)



# Start controller on switches (if any!)
c0.start()
s1.start([c0])
s2.start([c0])
sr.start([c0])

# Start CLI and build the network

net.build()
net.start()
# static arp
h1.cmd("arp -s 10.0.2.1 00:00:00:00:00:04")
h2.cmd("arp -s 10.0.1.1 00:00:00:00:00:03")

CLI(net)
net.stop()

