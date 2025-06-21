import joblib
import numpy as np
import pandas as pd
import os
import warnings

class AttackDetector:
    """
    This class loads a pre-trained machine learning model (KNN)
    and provides a prediction interface for network flow data.
    """

    def __init__(self, model_path: str = None):
        """
        Initialize the detector by loading the serialized model from disk.

        :param model_path: Path to the directory containing the saved .pkl model
        """

        if model_path is None:
            model_path = os.path.join('.', 'models', 'ownmodel')
        
        file = os.path.join(model_path, "knn_model.pkl")
        self.model = joblib.load(file)

    def predict(self, new_data_df) -> np.ndarray:
        """
        Predicts the label for the given network flow features.

        :param new_data_df: A dictionary or DataFrame with the expected features
        :return: A string label corresponding to the predicted attack type
        """
        # List of expected features (must match model training input)
        selected_features = [
            'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
            'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
            'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
            'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std',
            'Flow Bytes/s', 'Flow Packets/s', 'Fwd Packets/s', 'Bwd Packets/s',
            'Min Packet Length', 'Max Packet Length', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
            'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
            'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
            'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
            'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
            'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags'
        ]

        # Convert ordered dictionary into a NumPy array in correct shape
        ordered_features = list(new_data_df.keys())
        X_test = np.array([new_data_df[feat] for feat in ordered_features]).reshape(1, -1)

        # Map numerical prediction to a human-readable label
        label_map = {
            0: "BENIGN",
            1: "HULK",
            2: "SYNFLOOD",
            3: "UDPFLOOD",
            4: "POSTFLOOD"
        }

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)  # Suppress warnings from model
                prediction = self.model.predict(X_test)[0]
                label = label_map.get(prediction, "UNKNOWN")
                return label
        finally:
            print("Prediction completed")


# Example use case for debugging
if __name__ == "__main__":
    detector = AttackDetector()

    # Simulated input flow with all required features
    HULK = {
        'Destination Port': 8080, 'Flow Duration': 13.58, 'Total Fwd Packets': 2502,
        'Total Backward Packets': 0, 'Total Length of Fwd Packets': 235897.0,
        'Total Length of Bwd Packets': 0, 'Fwd Packet Length Max': 512.0,
        'Fwd Packet Length Min': 66.0, 'Fwd Packet Length Mean': 94.28, 'Fwd Packet Length Std': 97.0,
        'Bwd Packet Length Max': 0, 'Bwd Packet Length Min': 0, 'Bwd Packet Length Mean': 0,
        'Bwd Packet Length Std': 0, 'Flow Bytes/s': 17365.47, 'Flow Packets/s': 184.18,
        'Fwd Packets/s': 184.18, 'Bwd Packets/s': 0.0, 'Min Packet Length': 66.0,
        'Max Packet Length': 512.0, 'Packet Length Mean': 94.28, 'Packet Length Std': 97.0,
        'Packet Length Variance': 9409.67, 'Flow IAT Mean': 0.0054, 'Flow IAT Std': 0.2545,
        'Flow IAT Max': 12.71, 'Flow IAT Min': 0.000001, 'Fwd IAT Total': 13.58,
        'Fwd IAT Mean': 0.0054, 'Fwd IAT Std': 0.2545, 'Fwd IAT Max': 12.71,
        'Fwd IAT Min': 0.000001, 'Bwd IAT Total': 0, 'Bwd IAT Mean': 0,
        'Bwd IAT Std': 0, 'Bwd IAT Max': 0, 'Bwd IAT Min': 0,
        'FIN Flag Count': 726, 'SYN Flag Count': 628, 'RST Flag Count': 26,
        'PSH Flag Count': 171, 'ACK Flag Count': 1874, 'Fwd PSH Flags': 171,
        'Bwd PSH Flags': 0, 'Fwd URG Flags': 0, 'Bwd URG Flags': 0
    }

    # Run the prediction and print result
    prediction = detector.predict(HULK)
    print(f"Prediction: {prediction}")
