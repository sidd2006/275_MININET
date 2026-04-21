# 275_MININET

# SDN Host Discovery Service

A POX-based SDN controller module that automatically detects and maintains a database of hosts in an OpenFlow network.

## Features
- Detects host join events in real time
- Maintains a host database (MAC, IP, Switch, Port)
- Displays host details dynamically on every update

## Requirements
- Python 3
- POX SDN Controller
- Mininet

## Setup

Clone POX and place `host_discovery.py` in the `ext/` folder:

```bash
git clone https://github.com/noxrepo/pox
cp host_discovery.py pox/ext/
```

## Usage

**Terminal 1 - Start POX controller:**

```bash
cd pox
./pox.py host_discovery forwarding.l2_learning
```

**Terminal 2 - Start Mininet:**

```bash
sudo mn --topo single,3 --controller remote
```

**Inside Mininet, trigger host discovery:**

```bash
mininet> pingall
```

## How It Works

POX listens for PacketIn events from the switch. When a new packet arrives, the source MAC, switch DPID, and port are extracted and stored. ARP packets are parsed to resolve IP addresses, which update dynamically as traffic flows.

## File Structure
pox/
└── ext/
└── host_discovery.py
