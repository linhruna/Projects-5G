Overview

SliceSim is a simulation suite for network slicing in 5G networks.
The system models a network consisting of base stations and mobile clients, enabling researchers to analyze how different network slicing configurations affect resource allocation and network performance.

The simulator is based on discrete-event simulation and allows flexible configuration of network topology, slice parameters, and user mobility patterns.

This tool can be used to study concepts such as:

Network slicing resource allocation

Bandwidth utilization across slices

Client mobility impact on network performance

Blocking probability under heavy traffic

Proof-of-concept experiments for 5G slicing algorithms

Features
Network Slicing Simulation

Simulates multiple 5G network slices with different QoS requirements such as:

latency tolerance

guaranteed bandwidth

maximum bandwidth

Each base station allocates resources to slices based on configurable ratios.

Client Traffic Modeling

Clients generate traffic requests using configurable statistical distributions:

Uniform / Random distributions

Custom traffic generation patterns

Slice-based subscription ratios

Mobility Simulation

Supports configurable client mobility patterns, allowing simulation of realistic user movement across base stations.

Discrete Event Simulation

The system is implemented using SimPy, enabling efficient simulation of time-based network events.

Visualization and Statistics

After simulation, the system can generate:

Network statistics

Traffic distribution plots

Performance graphs

using Matplotlib.

Technologies Used

Python 3

SimPy

NumPy

Matplotlib

KDTree (for nearest base station search)

YAML configuration files

Asynchronous programming
### Example Output
![Example output for 5000 client in 3600s](https://github.com/cerob/slicesim/blob/master/examples/output_n5000_t3600.png)

