import matplotlib.pyplot as plt

class Visualizer:
    def plot(self, data):
        plt.figure(figsize=(8,4))
        plt.plot(data['Close'])
        plt.title("Price Graph")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.show()