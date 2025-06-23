import tkinter as tk
from tkinter import messagebox
import random
import string
from datetime import datetime

class PasswordGeneratorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Passwort Generator")
        self.window.geometry("550x500")
        self.window.configure(bg="#f0f0f0")
        
        # Zeichen-Sets
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%&*+-=?"
        
        # Historie
        self.password_history = []
        
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
        
        # Länge
        length_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Einstellungen",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        length_frame.pack(fill=tk.X, pady=(0, 10))
        
        slider_frame = tk.Frame(length_frame, bg="#f0f0f0")
        slider_frame.pack(fill=tk.X)
        
        tk.Label(
            slider_frame,
            text="Länge:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(
            slider_frame,
            from_=4,
            to=32,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg="#f0f0f0",
            length=200,
            command=self.update_length_label
        )
        self.length_scale.pack(side=tk.LEFT, padx=10)
        
        self.length_label = tk.Label(
            slider_frame,
            text="12",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2196F3"
        )
        self.length_label.pack(side=tk.LEFT)
        
        # Optionen
        options_grid = tk.Frame(length_frame, bg="#f0f0f0")
        options_grid.pack(fill=tk.X, pady=10)
        
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_grid,
            text="Großbuchstaben",
            variable=self.use_uppercase,
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w")
        
        tk.Checkbutton(
            options_grid,
            text="Zahlen",
            variable=self.use_digits,
            bg="#f0f0f0"
        ).grid(row=0, column=1, sticky="w")
        
        tk.Checkbutton(
            options_grid,
            text="Sonderzeichen",
            variable=self.use_special,
            bg="#f0f0f0"
        ).grid(row=1, column=0, sticky="w")
        
        # Buttons
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.generate_button = tk.Button(
            buttons_frame,
            text="🎲 1 Passwort",
            command=self.generate_single,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15
        )
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.multi_button = tk.Button(
            buttons_frame,
            text="🔢 5 Passwörter",
            command=self.generate_multiple,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15
        )
        self.multi_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.history_button = tk.Button(
            buttons_frame,
            text="📜 Historie",
            command=self.show_history,
            bg="#795548",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12
        )
        self.history_button.pack(side=tk.RIGHT)
        
        # Aktuelles Passwort
        current_frame = tk.LabelFrame(
            main_frame,
            text="🎯 Aktuelles Passwort",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        current_frame.pack(fill=tk.X, pady=10)
        
        password_frame = tk.Frame(current_frame, bg="#f0f0f0")
        password_frame.pack(fill=tk.X)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Courier", 14, "bold"),
            bg="#ffffff",
            fg="#2196F3",
            state="readonly"
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.copy_button = tk.Button(
            password_frame,
            text="📋 Kopieren",
            command=self.copy_current,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.copy_button.pack(side=tk.RIGHT)
        
        self.strength_label = tk.Label(
            current_frame,
            text="Noch kein Passwort generiert",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.strength_label.pack(anchor="w", pady=(5, 0))
    
    def update_length_label(self, value):
        self.length_label.config(text=str(value))
    
    def get_character_set(self):
        chars = self.lowercase
        if self.use_uppercase.get():
            chars += self.uppercase
        if self.use_digits.get():
            chars += self.digits
        if self.use_special.get():
            chars += self.special_chars
        return chars
    
    def create_password(self, length):
        chars = self.get_character_set()
        return ''.join(random.choice(chars) for _ in range(length))
    
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
    
    def add_to_history(self, password):
        timestamp = datetime.now().strftime("%H:%M:%S")
        strength = self.evaluate_strength(password)
        
        entry = {
            "password": password,
            "time": timestamp,
            "length": len(password),
            "strength": strength['text']
        }
        
        self.password_history.append(entry)
        
        # Nur letzte 20 behalten
        if len(self.password_history) > 20:
            self.password_history = self.password_history[-20:]
    
    def generate_single(self):
        length = self.length_var.get()
        password = self.create_password(length)
        
        self.password_var.set(password)
        
        strength = self.evaluate_strength(password)
        self.strength_label.config(text=f"Stärke: {strength['text']}", fg=strength['color'])
        
        self.add_to_history(password)
    
    def generate_multiple(self):
        length = self.length_var.get()
        passwords = []
        
        for _ in range(5):
            password = self.create_password(length)
            passwords.append(password)
            self.add_to_history(password)
        
        # Neues Fenster für Multiple
        multi_window = tk.Toplevel(self.window)
        multi_window.title("🔢 5 generierte Passwörter")
        multi_window.geometry("450x350")
        multi_window.configure(bg="#f0f0f0")
        
        tk.Label(
            multi_window,
            text="🔢 5 neue Passwörter:",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        text_widget = tk.Text(
            multi_window,
            font=("Courier", 12),
            bg="#ffffff",
            height=12
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for i, pwd in enumerate(passwords, 1):
            strength = self.evaluate_strength(pwd)
            text_widget.insert(tk.END, f"{i}. {pwd} ({strength['text']})\n\n")
        
        text_widget.config(state=tk.DISABLED)
        
        def copy_all():
            multi_window.clipboard_clear()
            multi_window.clipboard_append('\n'.join(passwords))
            messagebox.showinfo("Kopiert", "Alle 5 Passwörter kopiert!")
        
        tk.Button(
            multi_window,
            text="📋 Alle kopieren",
            command=copy_all,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=10)
    
    def show_history(self):
        if not self.password_history:
            messagebox.showinfo("Historie", "Noch keine Passwörter generiert!")
            return
        
        history_window = tk.Toplevel(self.window)
        history_window.title("📜 Passwort-Historie")
        history_window.geometry("500x400")
        history_window.configure(bg="#f0f0f0")
        
        tk.Label(
            history_window,
            text=f"📜 Historie ({len(self.password_history)} Passwörter):",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        # Scrollbares Text-Widget
        text_frame = tk.Frame(history_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_widget = tk.Text(text_frame, font=("Courier", 10))
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Letzte zuerst anzeigen
        for entry in reversed(self.password_history):
            text_widget.insert(tk.END, 
                f"{entry['time']} | {entry['password']} | {entry['strength']}\n")
        
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(
            history_window,
            text="🗑️ Historie löschen",
            command=lambda: self.clear_history(history_window),
            bg="#f44336",
            fg="white"
        ).pack(pady=10)
    
    def clear_history(self, window):
        if messagebox.askyesno("Bestätigen", "Historie wirklich löschen?"):
            self.password_history.clear()
            messagebox.showinfo("Gelöscht", "Historie wurde geleert!")
            window.destroy()
    
    def copy_current(self):
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