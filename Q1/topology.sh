#!/bin/bash

# deleleting previous namespaces and bridges
# command this part for the first run to avoid existence error!
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo ip -all netns delete
sudo ip link delete br1
sudo ip link delete br2

# create network namespaces
sudo ip netns add router
sudo ip netns add node1
sudo ip netns add node2
sudo ip netns add node3
sudo ip netns add node4

# create veth pair
sudo ip link add node1-veth type veth peer name br1-veth2
sudo ip link add node2-veth type veth peer name br1-veth3
sudo ip link add node3-veth type veth peer name br2-veth2
sudo ip link add node4-veth type veth peer name br2-veth3
sudo ip link add router-veth1 type veth peer name br1-veth1
sudo ip link add router-veth2 type veth peer name br2-veth1

# add veth to respective namespaces
sudo ip link set node1-veth netns node1
sudo ip link set node2-veth netns node2
sudo ip link set node3-veth netns node3
sudo ip link set node4-veth netns node4
sudo ip link set router-veth1 netns router
sudo ip link set router-veth2 netns router

# set ip addresses
sudo ip netns exec node1 ip addr add 172.0.0.2/24 dev node1-veth
sudo ip netns exec node2 ip addr add 172.0.0.3/24 dev node2-veth
sudo ip netns exec node3 ip addr add 10.10.0.2/24 dev node3-veth
sudo ip netns exec node4 ip addr add 10.10.0.3/24 dev node4-veth
sudo ip netns exec router ip addr add 172.0.0.1/24 dev router-veth1
sudo ip netns exec router ip addr add 10.10.0.1/24 dev router-veth2

# create bridges
sudo ip link add name br1 type bridge
sudo ip link add name br2 type bridge
sudo ip link set br1-veth1 master br1
sudo ip link set br1-veth2 master br1
sudo ip link set br1-veth3 master br1
sudo ip link set br2-veth1 master br2
sudo ip link set br2-veth2 master br2
sudo ip link set br2-veth3 master br2

# bring up interfaces
sudo ip netns exec node1 ip link set node1-veth up
sudo ip netns exec node2 ip link set node2-veth up
sudo ip netns exec node3 ip link set node3-veth up
sudo ip netns exec node4 ip link set node4-veth up
sudo ip netns exec router ip link set router-veth1 up
sudo ip netns exec router ip link set router-veth2 up

sudo ip netns exec node1 ip link set lo up
sudo ip netns exec node2 ip link set lo up
sudo ip netns exec node3 ip link set lo up
sudo ip netns exec node4 ip link set lo up
sudo ip netns exec router ip link set lo up

sudo ip link set br1 up
sudo ip link set br2 up
sudo ip link set br1-veth1 up
sudo ip link set br1-veth2 up
sudo ip link set br1-veth3 up
sudo ip link set br2-veth1 up
sudo ip link set br2-veth2 up
sudo ip link set br2-veth3 up

# add routes
sudo ip netns exec node1 ip route add default via 172.0.0.1
sudo ip netns exec node2 ip route add default via 172.0.0.1
sudo ip netns exec node3 ip route add default via 10.10.0.1
sudo ip netns exec node4 ip route add default via 10.10.0.1

