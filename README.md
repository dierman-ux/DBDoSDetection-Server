# blacklist_server

Real-time DoS attack detection and blockchain-based logging system using VeChain.

##  Overview

This project is a modular network security tool that captures traffic, extracts behavioral features, classifies flows using a trained ML model, and logs detected attacks into the VeChain testnet via smart contracts. It includes a web interface to manage the blacklist and interact with the system.

##  Project Structure

```
.
├── Blockchain/                      → Smart contract source code for both HLF and VeChain
│   ├── HLF/                         → Chaincode written in Go for Hyperledger Fabric
│   │   └── chaincode.go
│   └── VeChain/                     → Smart contract in Solidity for VeChainThor
│       └── smartcontract.sol
│
├── models/                          → Dataset and script used to train and export ML models
│   ├── knngenerator.py              → Script for training and exporting the KNN model
│   └── dataset.csv                  → Final preprocessed and labeled dataset for training
│
├── client/                          → Traffic simulator to generate test flows
│   └── client.py                    → Simulates benign and various DoS attack patterns
│
├── DoSDetector/                     → Core detection logic and packet-level feature analysis
│   ├── metrics.py                   → Extracts statistical features from captured traffic
│   ├── logger.py                    → Central logging utility for all detection modules
│   ├── blacklist.py                 → Local blacklist logic and warning counter
│   ├── detection.py                 → KNN-based traffic classifier (loads trained model)
│   └── blacklist/                   → Node.js scripts for blockchain interaction (VeChain)
│       └── *.cjs
│
├── Server/                          → HTTP server and REST API for interacting with the system
│   ├── server.py                    → Multithreaded REST server exposing web interface
│   ├── blacklist.py                 → Handles server-side access to blockchain logging
│   └── blacklist/                   → Duplicate of blockchain scripts for server use
│       └── *.cjs
│
├── docs/                            → Documentation, annexes, visual diagrams and figures
│   ├── README.md                    → Project overview and execution instructions
│   ├── Annex_I_Model.md             → Details on dataset creation, training and results
│   ├── Annex_II_Blockchain.md       → Description of smart contract logic and deployment
│   └── ...                          → PlantUML, diagrams, performance plots, etc.
│
├── requirements.txt                 → Python dependencies for installing and running the system
└── README.md                        → Root-level README with project introduction
```

##  Setup

### Prerequisites

- Python 3.9 or higher  
- Node.js and npm  
- `ts-node` (only if using TypeScript)  
- Administrator/root access to capture network traffic  

### Installation

```bash
pip install -r requirements.txt
```

##  Usage

### 1. Start the HTTP server

```bash
python server.py
```

### 2. Run the traffic monitor and detection engine

```bash
python metrics.py --ip 192.168.1. --port 8080
```

### 3. Run the client to test the monitoring and detection
```bash
python client.py --type hulk -url http://192.168.1.1:8080 --duration 60
```
> ⚠️ May require elevated privileges to access network interfaces.

##  Features

- Real-time DoS detection (SYNFlood, Hulk, UDPFlood, etc.)  
- ML-based classification using a trained KNN model  
- IP warning system and automatic blacklisting  
- Blockchain logging via VeChain testnet  
- Web interface for visualization and control  
- Extensible and modular architecture  

## Documentation

The `docs/` folder includes the complete technical documentation:

- [Introduction](docs/01_introduction.md)
- [Detection Pipeline](docs/02_detection_pipeline.md)
- [Blacklist & Blockchain](docs/03_blacklist_blockchain.md)
- [Web Interface](docs/04_web_interface.md)
- [Testing & Results](docs/05_testing_results.md)
- [Cost Estimate](docs/06_cost_estimate.md)

## License

Free Usage
