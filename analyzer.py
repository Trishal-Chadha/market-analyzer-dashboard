import pandas as pd

class Analyzer:
    def __init__(self, data):
        self.data = data.copy()

        if 'Close' not in self.data.columns:
            raise ValueError("Close column missing!")

        self.data['Close'] = pd.to_numeric(self.data['Close'], errors='coerce')
        self.data.dropna(subset=['Close'], inplace=True)

    def average_price(self):
        return round(self.data['Close'].mean(), 2)

    def summary(self):
        return {
            "Max Price": round(self.data['Close'].max(), 2),
            "Min Price": round(self.data['Close'].min(), 2),
            "Average Price": self.average_price()
        }

    def moving_average(self, window=3):
        return self.data['Close'].rolling(window).mean()