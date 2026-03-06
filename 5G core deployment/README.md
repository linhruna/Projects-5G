Open5GS Kubernetes Deployment
Overview

This project demonstrates how to deploy a cloud-native 5G Core Network using Open5GS on Kubernetes.
The deployment follows a microservices architecture, where each Network Function (NF) runs as a separate container.

The system supports:

Deployment of Open5GS core components (AMF, SMF, UPF, NRF, etc.)

Multi-slice configuration

MongoDB subscriber database

WebUI for subscriber management

Simulated 5G RAN using UERANSIM

This project helps understand 5G Core architecture, network slicing, and cloud-native telecom deployment.

Architecture

Components included in this deployment:

Open5GS Core Network

AMF – Access and Mobility Management Function

SMF – Session Management Function

UPF – User Plane Function

NRF – Network Repository Function

Database

MongoDB (stores subscriber data)

RAN Simulation

UERANSIM gNB

UERANSIM UE

Management

Open5GS WebUI

Deployment is orchestrated using Kubernetes manifests.