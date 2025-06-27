# 00 – Pre-Execution Setup

Before running the system, it is essential to ensure that the machine learning model required by the detection engine is properly trained and available. You must also prepare the JavaScript runtime environment used for blockchain interactions.

## Objective

The detection module (`detection.py`) uses a trained classifier to detect malicious traffic. A model must be generated beforehand and saved at the expected location. Additionally, the Node.js blockchain interaction scripts must be set up using `npm`.

---

## Input Files and Directories

- `models/dataset.csv` – Labeled dataset used to train the model.
- `models/svmgenerator.py` – Script to train and export the classifier. Choose the any from the models folder
- Output: `models/ownmodel/model.pkl`
- `Server/blacklist/` – Blockchain interaction scripts (VeChain)
- `DoSDetector/blacklist/` – Blockchain interaction scripts (VeChain)

---

## Steps

### 1. Train the ML model

```bash
cd models
python random_forestgenerator.py
```

This script will:
- Load the dataset from `dataset.csv`
- Balance the classes using SMOTE
- Train a Random Forest classifier (nº estimators=100, criterion	gini)
- Save the model to `models/ownmodel/model.pkl`
- Generate a performance report: `classification_report.csv`
- Generate ROC curves
- Generate PCA scatter plot
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
