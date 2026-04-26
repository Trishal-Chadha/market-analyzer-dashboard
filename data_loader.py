import pandas as pd

class DataLoader:
    def load_data(self, file_path):
        return pd.read_csv(file_path)