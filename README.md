# Software Defined Mobile Networks (SDMN) - Spring 2023

Welcome to the Software Defined Mobile Networks (SDMN) course repository! This repository contains the projects completed as part of the SDMN course offered at Sharif University of Technology. The course covered various advanced concepts in network virtualization, software-defined networking (SDN), cloud-native networking, and LTE/5G technologies.

## Project Overview

### 1. Virtual Networks with Mininet and OpenDaylight (Project 1)

**Description**: This project aimed to create a virtual network using **Mininet** and **Open vSwitch (OVS)**, without a default controller, and implement flows manually using the `ovs-ofctl` command. Later, we extended the network by introducing the **OpenDaylight (ODL)** SDN controller to manage the network and automate flow control.

**Key Tasks**:
- **Mininet Setup**: Used Mininet to create a simple LAN topology and input flows manually using OpenFlow.
- **Router Implementation**: Created a router using an OVS switch and configured it to handle Layer 3 traffic.
- **OpenDaylight Integration**: Set up ODL as an SDN controller and configured it to manage the network.
- **RESTCONF with ODL**: Created RESTCONF APIs to control flows through ODL, and used Python to push these flows.
- **Minimum Weight Routing**: Implemented a minimum-cost path routing algorithm using **Dijkstra's algorithm** and **NetworkX** to calculate routes and push flows to the network.

**Implementation Details**:
- **Python Scripts**: Scripts to create networks, generate flows, and push flows using RESTCONF.
- **Open vSwitch & Mininet**: Tools used for virtual network setup and flow management.

**How to Run**:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pouria-D/SDMN-Spring2023.git
   cd SDMN-Spring2023/Project%201_Virtual_Networks
   ```
2. **Set Up Mininet and ODL**:
   Install Mininet and OpenDaylight, following the provided instructions.
3. **Run Scripts**:
   Use the `create_net.py` and `push_flows.py` scripts to set up and configure the network.

### 2. Cloud-Native Containers and Docker (Project 2)

**Description**: The second project focused on building cloud-native mobile networks using **containers** and **Docker**. The goal was to understand container networking, container runtimes, and Dockerization of services for virtualized mobile network functions.

**Key Tasks**:
- **Container Networking**: Created a network topology using **Linux network namespaces** and **bridges**. Developed a bash script to create a network with multiple namespaces, routers, and bridges.
- **Container Runtime Implementation**: Implemented a simple container runtime similar to Docker, using **Linux namespaces** for networking, PID, mount, and UTS isolation. Created a CLI to manage containers.
- **Docker HTTP Server**: Developed an HTTP server with a simple API (`/api/v1/status`) that handled GET and POST requests, and dockerized it.

**Implementation Details**:
- **Linux Network Namespaces**: Used for container networking.
- **Custom Container Runtime**: Implemented in Python, allowing for container creation and management.
- **Docker HTTP Server**: A simple server that handles GET and POST requests, dockerized for containerization.

**How to Run**:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pouria-D/SDMN-Spring2023.git
   cd SDMN-Spring2023/Project%202_Cloud_Native
   ```
2. **Run Network Scripts**:
   Use the `create_topology.sh` script to set up container networking.
3. **Build and Run Docker Image**:
   Use the provided Dockerfile to build the HTTP server image:
   ```bash
   docker build -t sdmn-http-server .
   docker run -p 8000:8000 sdmn-http-server
   ```

### 3. Securing SDMN Using Microservices (Project 3)

**Description**: The final project focused on implementing security in SDMN using microservices architecture. The project explored container-based service deployment for mobile networks and used **OpenDaylight** as an SDN controller to manage secure traffic flow.

**Key Tasks**:
- **Microservices Architecture**: Deployed network functions as containerized microservices.
- **Service-Based Network Slicing**: Created different network slices using **containers** to deploy isolated services.
- **Traffic Management with ODL**: Used ODL to manage traffic flows across microservices and ensure isolation and security between slices.

**Implementation Details**:
- **OpenDaylight Controller**: Managed and monitored traffic flows.
- **Docker and Containers**: Used Docker to create isolated microservices for each network slice.
- **REST APIs**: Created REST APIs for traffic monitoring and management through ODL.

**How to Run**:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pouria-D/SDMN-Spring2023.git
   cd SDMN-Spring2023/Project%203_SDN_Security
   ```
2. **Deploy Containers**:
   Use Docker to deploy each microservice. Use ODL to manage and monitor the services.
3. **Run ODL Integration Scripts**:
   Use the provided scripts to connect microservices to the ODL controller and push flows.

## Requirements
- **Linux (Ubuntu 20.04 recommended)** for running Mininet, Open vSwitch, and Docker.
- **Python 3.8+** for scripting.
- **Docker** for containerization.
- **OpenDaylight** as an SDN controller.
- **Mininet** for network emulation.

## Contact
For any questions or additional information, feel free to contact me at [pouria.dadkhah@gmail.com](mailto:pouria.dadkhah@gmail.com).

---
Feel free to explore the projects, use the code for learning purposes, and contribute if you'd like to enhance the implementation!

