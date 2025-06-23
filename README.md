# blacklist_server

Real-time DoS attack detection and blockchain-based logging system using VeChain.

## Overview

This project is a modular network security tool that captures traffic, extracts behavioral features, classifies flows using a trained ML model, and logs detected attacks into the VeChain testnet via smart contracts. It includes a web interface to manage the blacklist and interact with the system.

## Project Structure

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
│   ├── randomforestgenerator.py     → Script for training and exporting the Random Forest model
│   ├── ...
│   └── DBDoS2025.csv                → Final preprocessed and labeled dataset for training
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
│   ├── 00_pre_execution.md          → How to train and prepare the model before running
│   └── ...
│
├── requirements.txt                 → Python dependencies for installing and running the system
└── README.md                        → This file
```

## Pre-Execution Setup

Before running the system, ensure a trained machine learning model is available at the expected path and the blockchain scripts are initialized.

### 1. Train the ML model
Choose your desired model based on script names.

```bash
cd models
python knngenerator.py
```

This will:
- Load the dataset (`DBDoS2025.csv`)
- Apply SMOTE to balance class distribution
- Train an appropiate model with the most suited hiperparameters
- Save the model in `models/ownmodel/model.pkl`
- Export `classification_report.csv` and other efficiency related data

### 2. Install Node.js dependencies

Make sure to run the following commands in both blacklist folders:

```bash
cd Server/blacklist
npm install

cd ../../DoSDetector/blacklist
npm install
```

These are required for VeChain blockchain logging to function properly.

## Setup

### Prerequisites

- Python 3.9 or higher  
- Node.js and npm  
- `ts-node` (only if using TypeScript)  
- Administrator/root access to capture network traffic  

### Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the HTTP server

```bash
python server.py
```

### 2. Run the traffic monitor and detection engine

```bash
python metrics.py --ip 192.168.1. --port 8080
```

> ⚠️ May require elevated privileges (e.g., `sudo`) to access network interfaces if in Linux OS.

### 3. Run the client to test the monitoring and detection

```bash
python client.py --type hulk --url http://192.168.1.1:8080 --duration 60
```

> ⚠️ May require elevated privileges (e.g., `sudo`) to access network interfaces.

## Features

- Real-time DoS detection (HULK, SYNFlood, UDPFlood, etc.)  
- ML-based classification using a trained KNN model  
- IP warning system and automatic blacklisting  
- Blockchain logging via VeChain testnet  
- Web interface for visualization and control  
- Extensible and modular architecture  

## Documentation

All technical documentation is available in the `docs/` directory:

- [00 – Pre-Execution Setup](docs/00_pre_execution.md)
- [01 – Introduction](docs/01_introduction.md)
- [02 – Detection Pipeline](docs/02_detection_pipeline.md)
- [03 – Blacklist & Blockchain](docs/03_blacklist_blockchain.md)
- [04 – Web Interface](docs/04_web_interface.md)
- [05 – Testing & Results](docs/05_testing_results.md)
- [06 – Cost Estimate](docs/06_cost_estimate.md)

## License

Free usage for academic and research purposes.
