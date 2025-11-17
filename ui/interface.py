import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import os

class CropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendación de Cultivo - UTP 2025")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f8ff")

        model_path = os.path.join(os.path.dirname(__file__), '../model_ml/best_rf_model.joblib')
        le_path = os.path.join(os.path.dirname(__file__), '../model_ml/label_encoder.joblib')
        self.model = joblib.load(model_path)
        self.le = joblib.load(le_path)

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self.root, text="RECOMENDADOR DE CULTIVOS INTELIGENTE", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        self.labels = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        self.entries = {}
        frame = ttk.Frame(self.root)
        frame.pack(pady=20)

        for i, label in enumerate(self.labels):
            ttk.Label(frame, text=label + ":", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=8, sticky="w")
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.entries[label] = entry

        btn = ttk.Button(self.root, text="PREDECIR CULTIVO", command=self.predict)
        btn.pack(pady=30)

        self.result_label = ttk.Label(self.root, text="", font=("Arial", 24, "bold"), foreground="green")
        self.result_label.pack(pady=40)

    def predict(self):
        try:
            features = [float(self.entries[key].get()) for key in self.labels]
            pred = self.model.predict([features])[0]
            crop = self.le.inverse_transform([pred])[0]
            self.result_label.config(text=f"CULTIVO ÓPTIMO:\n{crop.upper()}")
        except Exception as e:
            messagebox.showerror("Error", "Todos los campos deben ser numéricos")

if __name__ == "__main__":
    root = tk.Tk()
    app = CropApp(root)
    root.mainloop()
