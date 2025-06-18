import os
import ast
import pandas as pd

def parse_log_file(filepath, label):
    metrics = []
    with open(filepath, 'r') as f:
        for line in f:
            if "Metrics:" in line:
                try:
                    dict_start = line.index("{")
                    metrics_str = line[dict_start:]
                    metrics_dict = ast.literal_eval(metrics_str)
                    metrics_dict["label"] = label.upper()
                    metrics.append(metrics_dict)
                except Exception as e:
                    print(f"Error parsing line: {line}\n{e}")
    return metrics

def parse_all_logs(log_dir="."):
    all_data = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".log"):
            label = filename.replace(".log", "")
            path = os.path.join(log_dir, filename)
            print(f"Procesando {filename} como '{label.upper()}'")
            entries = parse_log_file(path, label)
            all_data.extend(entries)

    df = pd.DataFrame(all_data)
    df.to_csv("dataset.csv", index=False)
    print(f"[INFO] Guardado en dataset.csv con {len(df)} entradas.")

if __name__ == "__main__":
    parse_all_logs()
