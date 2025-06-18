import joblib
import numpy as np
import pandas as pd
import os
import warnings


class AttackDetector:
    def __init__(self, model_path: str = r'.\models\ownmodel'):
        """
        Inicializa el detector cargando el modelo entrenado.
        
        :param model_path: Ruta al archivo del modelo guardado (.pkl)
        """
        file=os.path.join(model_path, "knn_model.pkl")
        
        self.model = joblib.load(file)

    def predict(self, new_data_df) -> np.ndarray:
        """
        Predice etiquetas para el conjunto de características escaladas X.
        
        :param new_data_df: DataFrame con las características originales
        :return: Array con las predicciones (0 = normal, 1 = ataque)
        """
        selected_features = [
            'Destination Port',
            'Flow Duration',
            'Total Fwd Packets',
            'Total Backward Packets',
            'Total Length of Fwd Packets',
            'Total Length of Bwd Packets',
            'Fwd Packet Length Max',
            'Fwd Packet Length Min',
            'Fwd Packet Length Mean',
            'Fwd Packet Length Std',
            'Bwd Packet Length Max',
            'Bwd Packet Length Min',
            'Bwd Packet Length Mean',
            'Bwd Packet Length Std',
            'Flow Bytes/s',
            'Flow Packets/s',
            'Fwd Packets/s',
            'Bwd Packets/s',
            'Min Packet Length',
            'Max Packet Length',
            'Packet Length Mean',
            'Packet Length Std',
            'Packet Length Variance',
            'Flow IAT Mean',
            'Flow IAT Std',
            'Flow IAT Max',
            'Flow IAT Min',
            'Fwd IAT Total',
            'Fwd IAT Mean',
            'Fwd IAT Std',
            'Fwd IAT Max',
            'Fwd IAT Min',
            'Bwd IAT Total',
            'Bwd IAT Mean',
            'Bwd IAT Std',
            'Bwd IAT Max',
            'Bwd IAT Min',
            'FIN Flag Count',
            'SYN Flag Count',
            'RST Flag Count',
            'PSH Flag Count',
            'ACK Flag Count',
            'Fwd PSH Flags',
            'Bwd PSH Flags',
            'Fwd URG Flags',
            'Bwd URG Flags'
        ]


        ordered_features = list(new_data_df.keys())
        X_test = np.array([new_data_df[feat] for feat in ordered_features]).reshape(1, -1)
        # Mapeo de etiquetas numéricas a texto
        label_map = {
            0: "BENIGN",
            1: "HULK",
            2: "SYNFLOOD",
            3: "UDPFLOOD",
            4: "POSTFLOOD"
        }
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                prediction = self.model.predict(X_test)[0]
                label = label_map.get(prediction, "UNKNOWN")
                return label
        finally:
            print(f"Predicción realizada")


        

if __name__ == "__main__":
    detector = AttackDetector()
    
    slowloris = {'Destination Port': 8080, 'Flow Duration': 13.584256887435913, 'Total Fwd Packets': 2502, 'Total Backward Packets': 0, 'Total Length of Fwd Packets': 235897.0, 'Total Length of Bwd Packets': 0, 'Fwd Packet Length Max': 512.0, 'Fwd Packet Length Min': 66.0, 'Fwd Packet Length Mean': 94.2833733013589, 'Fwd Packet Length Std': 97.003440667487, 'Bwd Packet Length Max': 0, 'Bwd Packet Length Min': 0, 'Bwd Packet Length Mean': 0, 'Bwd Packet Length Std': 0, 'Flow Bytes/s': 17365.469598722128, 'Flow Packets/s': 184.18379604659134, 'Fwd Packets/s': 184.18379604659134, 'Bwd Packets/s': 0.0, 'Min Packet Length': 66.0, 'Max Packet Length': 512.0, 'Packet Length Mean': 94.2833733013589, 'Packet Length Std': 97.003440667487, 'Packet Length Variance': 9409.66750133067, 'Flow IAT Mean': 0.005431530142917198, 'Flow IAT Std': 0.25456656888904, 'Flow IAT Max': 12.715877056121826, 'Flow IAT Min': 9.5367431640625e-07, 'Fwd IAT Total': 13.584256887435913, 'Fwd IAT Mean': 0.005431530142917198, 'Fwd IAT Std': 0.25456656888904, 'Fwd IAT Max': 12.715877056121826, 'Fwd IAT Min': 9.5367431640625e-07, 'Bwd IAT Total': 0, 'Bwd IAT Mean': 0, 'Bwd IAT Std': 0, 'Bwd IAT Max': 0, 'Bwd IAT Min': 0, 'FIN Flag Count': 726, 'SYN Flag Count': 628, 'RST Flag Count': 26, 'PSH Flag Count': 171, 'ACK Flag Count': 1874, 'Fwd PSH Flags': 171, 'Bwd PSH Flags': 0, 'Fwd URG Flags': 0, 'Bwd URG Flags': 0}


    # Predicción
    prediction = detector.predict(slowloris) # -1 para ataque, 1 para benigno

    print(f"Predicción: {prediction}")