"""
In the name of god
SDMN HW1
Pouria Dadkhah - 401201381


Q1. Part2:

in this part hosts don't reach each other and are in different subnets so first they should understand the proper destination for
their packets and then send ip or icmp packets
to this, we set mac of router for their destination and router rearange the packet properely to give the packets to main destinations
in this case it's enough to set an static arp for each host to avoid sending arp flows in the network
mac 04 is set for first host des and 03 is set for second host dest and router should modify source and destintation of each packet

the corresponding flows on mininet shell should be like this:
sh ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:01,action=output:1
sh ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:04,action=output:2

sh ovs-ofctl add-flow s2 dl_dst=00:00:00:00:00:02,action=output:1
sh ovs-ofctl add-flow s2 dl_dst=00:00:00:00:00:03,action=output:2

sh ovs-ofctl add-flow r1 ip,nw_dst=10.0.1.0/24,actions=dec_ttl,mod_dl_dst:00:00:00:00:00:01,mod_dl_src:00:00:00:00:00:04,output:1
sh ovs-ofctl add-flow r1 ip,nw_dst=10.0.2.0/24,actions=dec_ttl,mod_dl_dst:00:00:00:00:00:02,mod_dl_src:00:00:00:00:00:03,output:2

we build the network from the sample code in question and just add hosts switches and links as requested with no controller

** they have been added extra flows in screenshot for handling arp flows in switches that they are not needed:
they should just act port actions based on des mac:

sh ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,action=flood
sh ovs-ofctl add-flow s2 dl_type=0x806,nw_proto=1,action=flood

the results are attached in screenshot

"""
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

setLogLevel( 'info' )


net = Mininet(controller=None,
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
    name="r1"
)
s2 = net.addSwitch(
    name="s2"
)
"""
# Adding controller (if any!)
c1 = net.addController(
    name = "your controller name"
    # Add an 'ip' and 'port' argument if you are
    # using a remote controller
)
"""

# Adding links
net.addLink(h1, s1)
net.addLink(h2, s2)
net.addLink(s1, sr)
net.addLink(sr, s2)

"""
# Start controller on switches (if any!)
s1.start([c1])  # More than one controller is possible!
"""
# Start CLI and build the network

net.build()
net.start()

h1.cmd("arp -s 10.0.2.1 00:00:00:00:00:04")
h2.cmd("arp -s 10.0.1.1 00:00:00:00:00:03")
CLI(net)
net.stop()

