import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Passwort Generator")
        self.window.geometry("400x500")
        self.window.configure(bg="#f0f0f0")
        
        # Zeichen-Sets
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%&*+-=?"
        
        self.setup_gui()
    
    def setup_gui(self):
        # Titel
        title_label = tk.Label(
            self.window,
            text="🔐 Passwort Generator",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2196F3"
        )
        title_label.pack(pady=20)
        
        # Länge-Eingabe
        length_frame = tk.Frame(self.window, bg="#f0f0f0")
        length_frame.pack(pady=10)
        
        tk.Label(
            length_frame,
            text="Passwort-Länge:",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        self.length_entry = tk.Entry(length_frame, width=5, justify="center")
        self.length_entry.pack(side=tk.LEFT, padx=10)
        self.length_entry.insert(0, "12")
        
        # Optionen
        options_frame = tk.Frame(self.window, bg="#f0f0f0")
        options_frame.pack(pady=20)
        
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_frame,
            text="Großbuchstaben",
            variable=self.use_uppercase,
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        tk.Checkbutton(
            options_frame,
            text="Zahlen",
            variable=self.use_digits,
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        tk.Checkbutton(
            options_frame,
            text="Sonderzeichen",
            variable=self.use_special,
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        # Generate Button
        self.generate_button = tk.Button(
            self.window,
            text="🎲 Passwort generieren",
            command=self.generate_password,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=10
        )
        self.generate_button.pack(pady=20)
        
        # Passwort-Anzeige
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            self.window,
            textvariable=self.password_var,
            font=("Courier", 14),
            justify="center",
            width=30,
            state="readonly"
        )
        self.password_entry.pack(pady=10)
        
        # Copy Button
        self.copy_button = tk.Button(
            self.window,
            text="📋 Kopieren",
            command=self.copy_password,
            bg="#FF9800",
            fg="white"
        )
        self.copy_button.pack(pady=5)
    
    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 4 or length > 50:
                messagebox.showwarning("Warnung", "Länge muss zwischen 4 und 50 sein!")
                return
        except ValueError:
            messagebox.showerror("Fehler", "Bitte gültige Zahl eingeben!")
            return
        
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
        
        messagebox.showinfo("Erfolg", "Neues Passwort generiert!")
    
    def copy_password(self):
        password = self.password_var.get()
        if password:
            self.window.clipboard_clear()
            self.window.clipboard_append(password)
            messagebox.showinfo("Kopiert", "Passwort in Zwischenablage kopiert!")
        else:
            messagebox.showwarning("Warnung", "Kein Passwort vorhanden!")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordGeneratorGUI()
    app.run()