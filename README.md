# blacklist_server

Real-time DoS attack detection and blockchain-based logging system using VeChain.

##  Overview

This project is a modular network security tool that captures traffic, extracts behavioral features, classifies flows using a trained ML model, and logs detected attacks into the VeChain testnet via smart contracts. It includes a web interface to manage the blacklist and interact with the system.

##  Project Structure

```
.
├── server.py              → REST HTTP server with web interface  
├── metrics.py             → Traffic capture and feature extraction (Scapy)  
├── detection.py           → Machine learning-based attack detection  
├── logger.py              → Unified logger configuration  
├── blacklist/             → Node.js/CJS scripts to interact with VeChain  
│   ├── sendAttackLog.cjs  
│   ├── getAttack.cjs  
│   └── ...  
├── frontend/              → Interactive HTML interface  
│   └── frontend.html  
├── requirements.txt       → Python dependencies  
└── README.md              → This file  
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

## 📖 Documentation

The `docs/` folder includes the complete technical documentation:

- `docs/01_introduction.md` → Project background and goals  
- `docs/02_detection_pipeline.md` → Feature extraction and ML logic  
- `docs/03_blacklist_blockchain.md` → VeChain integration  
- `docs/04_web_interface.md` → Frontend behavior and API  
- `docs/05_testing_results.md` → Metrics, performance, plots  
- `docs/06_cost_estimate.md` → Hardware/software/token costs  

## 📝 License

Free Usage