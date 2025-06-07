"""
detection.py

DetectionEngine class for traffic classification based on network flow features.

Features:
- Loads pre-trained machine learning model, scaler, and label encoder from disk.
- Computes flow-related features (e.g., inter-arrival times statistics).
- Performs prediction to classify traffic type (e.g., BENIGN or attack).
- Modular methods for feature calculation and model inference.
- Designed for integration with HTTP request handlers or other detection systems.

Author: Rafael Malla Martinez
Date: 2025-06-06
"""

import numpy as np
import pandas as pd
import joblib
import os
import time

class DetectionEngine:
    def __init__(self, base_dir, model_path='knn_model.pkl', scaler_path='scaler.pkl', le_path='label_encoder.pkl'):
        """
        Initialize the DetectionEngine:
        - Load the trained KNN model, scaler, and label encoder from the specified directory.
        - Define the expected feature names for input data frames used for prediction.
        
        Parameters:
            base_dir (str): Directory where the model and related files are stored.
            model_path (str): Filename of the saved KNN model.
            scaler_path (str): Filename of the saved scaler object.
            le_path (str): Filename of the saved label encoder.
        """
        self.model = joblib.load(os.path.join(base_dir, model_path))
        self.scaler = joblib.load(os.path.join(base_dir, scaler_path))
        self.le = joblib.load(os.path.join(base_dir, le_path))

        self.feature_names = [
            'Fwd IAT Total', 'Flow Duration', 'Idle Max', 'Fwd IAT Max', 'Flow IAT Max',
            'Idle Mean', 'Idle Min', 'Bwd IAT Total', 'Bwd IAT Max', 'Fwd IAT Std',
            'Flow IAT Std', 'Fwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Mean'
        ]

    def detect(self, iat_forward, flow_start_time, iat_backward=None, idle_times=None):
        """
        Main detection function:
        - Calculate features based on input forward/backward inter-arrival times and flow start time.
        - Print the feature vector for debugging purposes.
        - Validate feature vector shape before prediction.
        - Return the predicted class label (e.g., benign or attack).
        
        Parameters:
            iat_forward (list): Forward inter-arrival times.
            flow_start_time (float): Timestamp when the flow started.
            iat_backward (list, optional): Backward inter-arrival times.
            idle_times (list, optional): Idle times within the flow.
        
        Returns:
            str: Predicted class label after decoding.
        """
        features_df = self.calcular_features(iat_forward, flow_start_time, iat_backward, idle_times)

        print(f"Feature vector for prediction:")
        for col, val in features_df.iloc[0].items():
            print(f"{col}: {val}")

        if features_df.shape[1] != len(self.feature_names):
            raise ValueError(f"Expected {len(self.feature_names)} features, got {features_df.shape[1]}")

        return self.predecir(features_df)

    def calcular_features(self, iat_forward, flow_start_time, iat_backward=None, idle_times=None):
        """
        Compute the feature vector for the detection model from raw input data:
        - Calculate flow duration based on current time and flow start time.
        - Compute statistics (total, max, mean, std, min) for forward and backward IATs and idle times.
        - Combine features into a single-row pandas DataFrame matching the expected input format.
        
        Parameters:
            iat_forward (list): Forward inter-arrival times.
            flow_start_time (float): Timestamp when the flow started.
            iat_backward (list, optional): Backward inter-arrival times.
            idle_times (list, optional): Idle times.
        
        Returns:
            pandas.DataFrame: DataFrame with one row containing all features.
        """
        flow_duration = time.time() - flow_start_time

        # Calculate forward IAT statistics
        fwd_iat_total = self.calc_total(iat_forward)
        fwd_iat_max = self.calc_max(iat_forward)
        fwd_iat_mean = self.calc_mean(iat_forward)
        fwd_iat_std = self.calc_std(iat_forward)

        # Calculate backward IAT statistics
        bwd_iat_total = self.calc_total(iat_backward)
        bwd_iat_max = self.calc_max(iat_backward)
        bwd_iat_mean = self.calc_mean(iat_backward)
        bwd_iat_std = self.calc_std(iat_backward)

        # Calculate idle time statistics
        idle_max = self.calc_max(idle_times)
        idle_mean = self.calc_mean(idle_times)
        idle_min = self.calc_min(idle_times)

        # Calculate flow IAT max and std by combining forward and backward IATs
        combined_iats = (iat_forward if iat_forward else []) + (iat_backward if iat_backward else [])
        flow_iat_max = self.calc_max(combined_iats)
        flow_iat_std = self.calc_std(combined_iats)

        # Assemble features in the order expected by the model
        features = np.array([
            fwd_iat_total, flow_duration, idle_max, fwd_iat_max, flow_iat_max,
            idle_mean, idle_min, bwd_iat_total, bwd_iat_max, fwd_iat_std,
            flow_iat_std, fwd_iat_mean, bwd_iat_std, bwd_iat_mean
        ]).reshape(1, -1)

        return pd.DataFrame(features, columns=self.feature_names)

    def calc_total(self, data):
        """
        Calculate the sum of values in a list.
        Return 0 if the input is None or empty.
        """
        if data:
            return np.sum(data)
        return 0

    def calc_max(self, data):
        """
        Calculate the maximum value in a list.
        Return 0 if the input is None or empty.
        """
        if data:
            return np.max(data)
        return 0

    def calc_min(self, data):
        """
        Calculate the minimum value in a list.
        Return 0 if the input is None or empty.
        """
        if data:
            return np.min(data)
        return 0

    def calc_mean(self, data):
        """
        Calculate the mean (average) of values in a list.
        Return 0 if the input is None or empty.
        """
        if data:
            return np.mean(data)
        return 0

    def calc_std(self, data):
        """
        Calculate the standard deviation of values in a list.
        Return 0 if the input is None or empty.
        """
        if data:
            return np.std(data)
        return 0

    def predecir(self, feature_vector_df):
        """
        Perform the prediction:
        - Scale the feature vector using the loaded scaler.
        - Predict the encoded class label using the loaded model.
        - Decode the predicted label to a human-readable class name.
        
        Parameters:
            feature_vector_df (pandas.DataFrame): DataFrame containing one row of features.
        
        Returns:
            str: Decoded predicted class label.
        """
        scaled_features = self.scaler.transform(feature_vector_df)
        prediction_encoded = self.model.predict(scaled_features)[0]
        return self.le.inverse_transform([prediction_encoded])[0]
