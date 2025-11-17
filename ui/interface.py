import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import os

class CropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendador de Cultivos - UTP 2025")
        self.root.geometry("900x750")
        self.root.configure(bg="#f0f8ff")

        # Rutas correctas (funciona en cualquier PC)
        base_path = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(base_path, "model_ml", "best_rf_model.joblib")
        le_path = os.path.join(base_path, "model_ml", "label_encoder.joblib")
        
        self.model = joblib.load(model_path)
        self.le = joblib.load(le_path)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="RECOMENDADOR DE CULTIVOS INTELIGENTE", 
                font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#006400").pack(pady=30)

        labels = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        self.entries = {}
        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(pady=20)

        for i, label in enumerate(labels):
            tk.Label(frame, text=label + ":", font=("Arial", 14), bg="#f0f8ff").grid(row=i, column=0, padx=15, pady=12, sticky="w")
            entry = tk.Entry(frame, width=25, font=("Arial", 14))
            entry.grid(row=i, column=1, padx=15, pady=12)
            self.entries[label] = entry

        tk.Button(self.root, text="PREDECIR CULTIVO", font=("Arial", 16, "bold"),
                 bg="#006400", fg="white", command=self.predict, height=2, width=25).pack(pady=40)

        self.result = tk.Label(self.root, text="", font=("Arial", 32, "bold"), bg="#f0f8ff", fg="#006400")
        self.result.pack(pady=50)

    def predict(self):
        try:
            values = [float(self.entries[k].get()) for k in ["N","P","K","temperature","humidity","ph","rainfall"]]
            pred = self.model.predict([values])[0]
            crop = self.le.inverse_transform([pred])[0].upper()
            self.result.config(text=f"→ {crop} ←")
        except Exception as e:
            messagebox.showerror("Error", "Todos los campos deben ser números válidos")

if __name__ == "__main__":
    root = tk.Tk()
    app = CropApp(root)
    root.mainloop()
