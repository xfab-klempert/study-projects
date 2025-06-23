import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Passwort Generator")
        self.window.geometry("500x550")
        self.window.configure(bg="#f0f0f0")
        
        # Zeichen-Sets
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%&*+-=?"
        
        self.setup_gui()
    
    def setup_gui(self):
        # Header
        header_frame = tk.Frame(self.window, bg="#2196F3", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Passwort Generator",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Main Frame
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Länge mit Schieberegler
        length_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Passwort-Länge",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        length_frame.pack(fill=tk.X, pady=(0, 15))
        
        slider_frame = tk.Frame(length_frame, bg="#f0f0f0")
        slider_frame.pack(fill=tk.X)
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(
            slider_frame,
            from_=4,
            to=32,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg="#f0f0f0",
            length=300,
            command=self.update_length_label
        )
        self.length_scale.pack(side=tk.LEFT)
        
        self.length_label = tk.Label(
            slider_frame,
            text="12 Zeichen",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2196F3"
        )
        self.length_label.pack(side=tk.RIGHT, padx=20)
        
        # Optionen
        options_frame = tk.LabelFrame(
            main_frame,
            text="🎯 Zeichen-Optionen",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_frame,
            text="✓ Großbuchstaben (A-Z)",
            variable=self.use_uppercase,
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(anchor="w", pady=2)
        
        tk.Checkbutton(
            options_frame,
            text="✓ Zahlen (0-9)",
            variable=self.use_digits,
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(anchor="w", pady=2)
        
        tk.Checkbutton(
            options_frame,
            text="  Sonderzeichen (!@#$%&*+-=?)",
            variable=self.use_special,
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(anchor="w", pady=2)
        
        # Generator
        generator_frame = tk.LabelFrame(
            main_frame,
            text="🎲 Generator",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        generator_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.generate_button = tk.Button(
            generator_frame,
            text="🎲 Neues Passwort generieren",
            command=self.generate_password,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=8
        )
        self.generate_button.pack(pady=10)
        
        # Passwort-Anzeige
        password_frame = tk.Frame(generator_frame, bg="#f0f0f0")
        password_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            password_frame,
            text="Generiertes Passwort:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        entry_frame = tk.Frame(password_frame, bg="#f0f0f0")
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            entry_frame,
            textvariable=self.password_var,
            font=("Courier", 14, "bold"),
            bg="#ffffff",
            fg="#2196F3",
            state="readonly"
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.copy_button = tk.Button(
            entry_frame,
            text="📋",
            command=self.copy_password,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=3
        )
        self.copy_button.pack(side=tk.RIGHT)
        
        # Stärke-Anzeige
        self.strength_label = tk.Label(
            password_frame,
            text="Noch kein Passwort generiert",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.strength_label.pack(anchor="w", pady=(5, 0))
    
    def update_length_label(self, value):
        self.length_label.config(text=f"{value} Zeichen")
    
    def evaluate_strength(self, password):
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in self.special_chars for c in password):
            score += 1
        
        if score >= 4:
            return {"text": "🟢 Stark", "color": "#4CAF50"}
        elif score >= 3:
            return {"text": "🟡 Mittel", "color": "#FF9800"}
        else:
            return {"text": "🔴 Schwach", "color": "#f44336"}
    
    def generate_password(self):
        length = self.length_var.get()
        
        # Zeichen sammeln
        chars = self.lowercase
        if self.use_uppercase.get():
            chars += self.uppercase
        if self.use_digits.get():
            chars += self.digits
        if self.use_special.get():
            chars += self.special_chars
        
        # Passwort generieren
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Stärke bewerten
        strength = self.evaluate_strength(password)
        self.strength_label.config(text=f"Stärke: {strength['text']}", fg=strength['color'])
    
    def copy_password(self):
        password = self.password_var.get()
        if password:
            self.window.clipboard_clear()
            self.window.clipboard_append(password)
            messagebox.showinfo("Kopiert", "Passwort kopiert!")
        else:
            messagebox.showwarning("Warnung", "Kein Passwort vorhanden!")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordGeneratorGUI()
    app.run()