# 00 – Pre-Execution Setup

Before running the system, it is essential to ensure that the machine learning model required by the detection engine is properly trained and available. You must also prepare the JavaScript runtime environment used for blockchain interactions.

## Objective

The detection module (`detection.py`) uses a trained KNN classifier to detect malicious traffic. This model must be generated beforehand and saved at the expected location. Additionally, the Node.js blockchain interaction scripts must be set up using `npm`.

---

## Input Files and Directories

- `models/dataset.csv` – Labeled dataset used to train the model.
- `models/knngenerator.py` – Script to train and export the classifier.
- Output: `models/ownmodel/knn_model.pkl`
- `Server/blacklist/` – Blockchain interaction scripts (VeChain)
- `DoSDetector/blacklist/` – Blockchain interaction scripts (VeChain)

---

## Steps

### 1. Train the ML model

```bash
cd models
python knngenerator.py
```

This script will:
- Load the dataset from `dataset.csv`
- Balance the classes using SMOTE
- Train a KNN classifier (k=5, Euclidean distance)
- Save the model to `models/ownmodel/knn_model.pkl`
- Generate a performance report: `classification_report.csv`
- Display a confusion matrix for visual evaluation

---

### 2. Install dependencies for blockchain scripts

Navigate to both folders containing VeChain interaction scripts and install dependencies:

```bash
cd Server/blacklist
npm install

cd ../../DoSDetector/blacklist
npm install
```

This will ensure `node-fetch`, `ethers`, or any other required dependencies are installed.

---

## Note

- The trained model will be automatically loaded during runtime by the `detection.py` module.
- Both `blacklist/` folders must be properly initialized with `npm install` before calling any `.cjs` scripts.
- No additional configuration is required after these steps.
