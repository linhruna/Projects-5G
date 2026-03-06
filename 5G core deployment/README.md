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
