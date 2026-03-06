## Overview
This project demonstrates the deployment of a cloud-native 5G Core Network using Open5GS on a Kubernetes cluster.  
The system uses microservices architecture where each Network Function (NF) runs as a separate containerized service.

The project also integrates UERANSIM to simulate a 5G gNB and multiple User Equipments (UEs) to test connectivity through the 5G core network.


## Architecture

The deployed 5G core includes the following network functions:

- AMF – Access and Mobility Management Function
- SMF – Session Management Function
- UPF – User Plane Function
- NRF – Network Repository Function
- UDM – Unified Data Management
- AUSF – Authentication Server Function
- NSSF – Network Slice Selection Function

Supporting components:

- MongoDB – stores subscriber and network data
- Open5GS WebUI – manage subscriber profiles
- Multus + OVS-CNI – multi-network interfaces in Kubernetes
- UERANSIM – simulated gNB and UE
