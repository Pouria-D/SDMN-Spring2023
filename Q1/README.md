Question 1

PART 1:

The topology creator shell and ping bash are as above and summary details has bee writen in their coments.

---------------

PART2:

In this part we bring up nodes and links like previous part just instead of setting default ip of nodes to 10.10.0.1 and 172.0.0.1, set that to server'ip.

so as result when packet enters to eache bridges because they are in the same namespacem they can see each other and we should just add a rout command to ip tabels as below:

sudo ip route add 172.0.0.0/24 dev br1

sudo ip route add 10.10.0.0/24 dev br2

---------------

PART3:

This part is similar to part2 just we should add the first rout command in server 1 and the second in server 2.

addintionally change the node1 and node2 default to first server'ip and the other two to second server'ip and add this rout command in first server and similar one to second:

sudo ip route add 10.10.0.0/24 via <ip-server2> .
