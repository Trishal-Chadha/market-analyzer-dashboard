import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from data_loader import DataLoader
from analyzer import Analyzer

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Market Analyzer Pro")
        self.root.geometry("900x550")
        self.root.configure(bg="#121212")

        self.loader = DataLoader()
        self.data = None
        self.current_dataset = None

        # ===== HEADER =====
        tk.Label(
            root,
            text="Market Analyzer Dashboard",
            bg="#121212",
            fg="#00ffcc",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # ===== MAIN FRAME =====
        main = tk.Frame(root, bg="#121212")
        main.pack(fill="both", expand=True)

        # ===== SIDEBAR =====
        sidebar = tk.Frame(main, bg="#1f1f2e", width=200)
        sidebar.pack(side="left", fill="y")

        tk.Button(sidebar, text="📈 Stock Data", command=self.load_stock, bg="#00b894", fg="white", width=18).pack(pady=10)
        tk.Button(sidebar, text="₿ Bitcoin Data", command=self.load_bitcoin, bg="#0984e3", fg="white", width=18).pack(pady=10)
        tk.Button(sidebar, text="🔄 Compare Both", command=self.compare_graph, bg="#6c5ce7", fg="white", width=18).pack(pady=10)

        # ===== CONTENT =====
        self.content = tk.Frame(main, bg="#121212")
        self.content.pack(side="right", fill="both", expand=True)

        tk.Button(self.content, text="📊 Show Summary", command=self.show_summary, bg="#fdcb6e", width=20).pack(pady=5)
        tk.Button(self.content, text="📈 Show Graph", command=self.show_graph, bg="#00cec9", width=20).pack(pady=5)
        tk.Button(self.content, text="📉 Moving Average", command=self.show_ma, bg="#d63031", width=20).pack(pady=5)

        # ===== GRAPH AREA =====
        self.graph_frame = tk.Frame(self.content, bg="#121212")
        self.graph_frame.pack(fill="both", expand=True)

    # ===== LOAD DATA =====
    def load_stock(self):
        self.data = self.loader.load_data("stock_data.csv")
        self.current_dataset = "Stock"
        messagebox.showinfo("Success", "Stock Data Loaded!")

    def load_bitcoin(self):
        self.data = self.loader.load_data("bitcoin_data.csv")
        self.current_dataset = "Bitcoin"
        messagebox.showinfo("Success", "Bitcoin Data Loaded!")

    # ===== CLEAR GRAPH =====
    def clear_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    # ===== EMBED GRAPH =====
    def draw_graph(self, fig):
        self.clear_graph()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ===== SHOW GRAPH =====
    def show_graph(self):
        if self.data is None:
            messagebox.showerror("Error", "Load data first!")
            return

        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(self.data['Close'], label=self.current_dataset)
        ax.set_title("Price Graph")
        ax.legend()

        self.draw_graph(fig)

    # ===== MOVING AVERAGE =====
    def show_ma(self):
        if self.data is None:
            messagebox.showerror("Error", "Load data first!")
            return

        analyzer = Analyzer(self.data)
        ma = analyzer.moving_average()

        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(self.data['Close'], label="Close")
        ax.plot(ma, label="Moving Avg")
        ax.legend()
        ax.set_title("Moving Average")

        self.draw_graph(fig)

    # ===== SUMMARY =====
    def show_summary(self):
        if self.data is None:
            messagebox.showerror("Error", "Load data first!")
            return

        analyzer = Analyzer(self.data)
        summary = analyzer.summary()

        msg = "\n".join([f"{k}: {v}" for k, v in summary.items()])
        messagebox.showinfo("Summary", msg)

    # ===== COMPARE GRAPH =====
    def compare_graph(self):
        try:
            stock = self.loader.load_data("stock_data.csv")
            btc = self.loader.load_data("bitcoin_data.csv")

            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(stock['Close'], label="Stock")
            ax.plot(btc['Close'], label="Bitcoin")

            ax.set_title("Stock vs Bitcoin")
            ax.legend()

            self.draw_graph(fig)

        except Exception as e:
            messagebox.showerror("Error", str(e))