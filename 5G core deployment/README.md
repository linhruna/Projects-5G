
## Overview
This project demonstrates the deployment of a cloud-native **5G Core Network** using **Open5GS** on **Kubernetes**.  
The system simulates a complete 5G Standalone (SA) environment by integrating Open5GS core network functions with **UERANSIM** to emulate gNB and UE devices.

The deployment follows a **microservices architecture**, where each 5G Network Function (NF) runs as an independent containerized service. The project supports **multi-slice configuration** and enables end-to-end connectivity testing within a simulated 5G network environment.

## Features
- Cloud-native 5G Core deployment using Kubernetes
- Containerized 5G Network Functions (AMF, SMF, UPF, etc.)
- Simulated 5G Radio Access Network using UERANSIM
- Multi-slice network configuration
- Subscriber management via Open5GS WebUI
- End-to-end connectivity testing

## System Architecture
The system includes the following components:

- **Open5GS** – 5G Core Network implementation
- **UERANSIM** – Simulation of gNB and UE
- **MongoDB** – Subscriber database
- **Kubernetes** – Container orchestration platform
- **Multus & OVS-CNI** – Multi-network configuration for 5G interfaces

## An example of Subscriber UI
<img width="2176" height="1232" alt="image" src="https://github.com/user-attachments/assets/badc5032-5274-4130-a20c-b44f015f1fec" />

