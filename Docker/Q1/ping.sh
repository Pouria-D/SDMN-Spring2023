#!/bin/bash

# src: node1-node2-node3-node4-router
# dst: node1-node2-node3-node4-router1-router2

case $2 in
	node1) ip_dst=172.0.0.2;;
	node2) ip_dst=172.0.0.3;;
	node3) ip_dst=10.10.0.2;;
	node4) ip_dst=10.10.0.3;;
	router1) ip_dst=172.0.0.1;;
	router2) ip_dst=10.10.0.1;;
esac

ip netns exec $1 ping $ip_dst

