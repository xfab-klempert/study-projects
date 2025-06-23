import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔐 Passwort Generator")
        self.window.geometry("600x550")
        self.window.configure(bg="#f0f0f0")
        self.window.resizable(True, True)
        
        # Passwort-Historie
        self.password_history = []
        
        # Zeichen-Sets
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%&*+-=?^_|~"
        self.ambiguous_chars = "il1Lo0O"
        
        self.setup_gui()
        self.load_settings()
        
    def setup_gui(self):
        # Header
        header_frame = tk.Frame(self.window, bg="#2196F3", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Sicherer Passwort Generator",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Main Content Frame
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Einstellungen Frame
        settings_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Passwort-Einstellungen",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            padx=15,
            pady=15
        )
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Passwort-Länge
        length_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        length_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            length_frame,
            text="Passwort-Länge:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(
            length_frame,
            from_=4,
            to=64,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg="#f0f0f0",
            length=200
        )
        self.length_scale.pack(side=tk.LEFT, padx=10)
        
        self.length_label = tk.Label(
            length_frame,
            text="12 Zeichen",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2196F3"
        )
        self.length_label.pack(side=tk.RIGHT)
        
        # Event-Binding für Length-Update
        self.length_scale.configure(command=self.update_length_label)
        
        # Zeichen-Optionen
        options_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Checkboxes für Zeichen-Typen
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_frame,
            text="Kleinbuchstaben (a-z)",
            variable=self.use_lowercase,
            font=("Arial", 10),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", padx=5)
        
        tk.Checkbutton(
            options_frame,
            text="Großbuchstaben (A-Z)",
            variable=self.use_uppercase,
            font=("Arial", 10),
            bg="#f0f0f0"
        ).grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Checkbutton(
            options_frame,
            text="Zahlen (0-9)",
            variable=self.use_digits,
            font=("Arial", 10),
            bg="#f0f0f0"
        ).grid(row=1, column=0, sticky="w", padx=5)
        
        tk.Checkbutton(
            options_frame,
            text="Sonderzeichen (!@#$...)",
            variable=self.use_special,
            font=("Arial", 10),
            bg="#f0f0f0"
        ).grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Checkbutton(
            options_frame,
            text="Mehrdeutige Zeichen ausschließen (il1Lo0O)",
            variable=self.exclude_ambiguous,
            font=("Arial", 10),
            bg="#f0f0f0"
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
        
        # Generator-Bereich
        generator_frame = tk.LabelFrame(
            main_frame,
            text="🎯 Passwort generieren",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            padx=15,
            pady=15
        )
        generator_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Generate Button
        self.generate_button = tk.Button(
            generator_frame,
            text="🎲 Neues Passwort generieren",
            command=self.generate_password,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10
        )
        self.generate_button.pack(pady=10)
        
        # Passwort-Anzeige
        password_display_frame = tk.Frame(generator_frame, bg="#f0f0f0")
        password_display_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            password_display_frame,
            text="Generiertes Passwort:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        # Passwort-Textfeld
        self.password_var = tk.StringVar()
        password_entry_frame = tk.Frame(password_display_frame, bg="#f0f0f0")
        password_entry_frame.pack(fill=tk.X, pady=5)
        
        self.password_entry = tk.Entry(
            password_entry_frame,
            textvariable=self.password_var,
            font=("Courier", 14, "bold"),
            bg="#ffffff",
            fg="#2196F3",
            relief=tk.RAISED,
            bd=2,
            state="readonly"
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Copy Button
        self.copy_button = tk.Button(
            password_entry_frame,
            text="📋 Kopieren",
            command=self.copy_password,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.copy_button.pack(side=tk.RIGHT)
        
        # Passwort-Stärke Anzeige
        strength_frame = tk.Frame(generator_frame, bg="#f0f0f0")
        strength_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            strength_frame,
            text="Passwort-Stärke:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        self.strength_label = tk.Label(
            strength_frame,
            text="Noch kein Passwort generiert",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#666666"
        )
        self.strength_label.pack(side=tk.LEFT, padx=10)
        
        # Buttons Frame
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Multiple Passwords Button
        self.multi_button = tk.Button(
            buttons_frame,
            text="🔢 5 Passwörter generieren",
            command=self.generate_multiple,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        self.multi_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Historie Button
        self.history_button = tk.Button(
            buttons_frame,
            text="📜 Historie anzeigen",
            command=self.show_history,
            bg="#795548",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        self.history_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export Button
        self.export_button = tk.Button(
            buttons_frame,
            text="💾 Exportieren",
            command=self.export_passwords,
            bg="#607D8B",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear Historie Button
        self.clear_button = tk.Button(
            buttons_frame,
            text="🗑️ Historie löschen",
            command=self.clear_history,
            bg="#f44336",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        self.clear_button.pack(side=tk.RIGHT)
        
    def update_length_label(self, value):
        self.length_label.config(text=f"{value} Zeichen")
        
    def build_character_set(self):
        chars = ""
        
        if self.use_lowercase.get():
            chars += self.lowercase
        if self.use_uppercase.get():
            chars += self.uppercase
        if self.use_digits.get():
            chars += self.digits
        if self.use_special.get():
            chars += self.special_chars
            
        # Mehrdeutige Zeichen entfernen
        if self.exclude_ambiguous.get():
            chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            
        return chars
    
    def generate_password(self):
        # Prüfen ob mindestens eine Option gewählt ist
        if not any([self.use_lowercase.get(), self.use_uppercase.get(), 
                   self.use_digits.get(), self.use_special.get()]):
            messagebox.showwarning("Warnung", "Bitte wähle mindestens eine Zeichen-Art aus!")
            return
            
        chars = self.build_character_set()
        
        if not chars:
            messagebox.showerror("Fehler", "Keine verfügbaren Zeichen für Passwort-Generierung!")
            return
            
        length = self.length_var.get()
        
        # Passwort generieren mit garantiertem Mix
        password = self.generate_mixed_password(chars, length)
        
        # Passwort anzeigen
        self.password_var.set(password)
        
        # Stärke bewerten
        strength = self.evaluate_password_strength(password)
        self.strength_label.config(text=strength['text'], fg=strength['color'])
        
        # Zur Historie hinzufügen
        self.add_to_history(password)
        
    def generate_mixed_password(self, chars, length):
        # Sicherstellen, dass jede gewählte Zeichen-Art mindestens einmal vorkommt
        password = []
        
        if self.use_lowercase.get():
            available_lower = [c for c in self.lowercase if c in chars]
            if available_lower:
                password.append(random.choice(available_lower))
                
        if self.use_uppercase.get():
            available_upper = [c for c in self.uppercase if c in chars]
            if available_upper:
                password.append(random.choice(available_upper))
                
        if self.use_digits.get():
            available_digits = [c for c in self.digits if c in chars]
            if available_digits:
                password.append(random.choice(available_digits))
                
        if self.use_special.get():
            available_special = [c for c in self.special_chars if c in chars]
            if available_special:
                password.append(random.choice(available_special))
        
        # Rest der Zeichen zufällig füllen
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(random.choice(chars))
            
        # Passwort mischen
        random.shuffle(password)
        
        return ''.join(password)
    
    def evaluate_password_strength(self, password):
        score = 0
        feedback = []
        
        # Länge bewerten
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
        else:
            feedback.append("zu kurz")
            
        # Zeichen-Vielfalt bewerten
        if any(c.islower() for c in password):
            score += 15
        if any(c.isupper() for c in password):
            score += 15
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in self.special_chars for c in password):
            score += 20
            
        # Keine Wiederholungen
        if len(set(password)) == len(password):
            score += 10
        else:
            feedback.append("wiederholte Zeichen")
            
        # Bewertung zurückgeben
        if score >= 85:
            return {"text": "🟢 Sehr stark", "color": "#4CAF50"}
        elif score >= 70:
            return {"text": "🟡 Stark", "color": "#FF9800"}
        elif score >= 50:
            return {"text": "🟠 Mittel", "color": "#FF5722"}
        else:
            return {"text": "🔴 Schwach", "color": "#f44336"}
    
    def copy_password(self):
        if self.password_var.get():
            self.window.clipboard_clear()
            self.window.clipboard_append(self.password_var.get())
            messagebox.showinfo("Kopiert", "Passwort wurde in die Zwischenablage kopiert!")
        else:
            messagebox.showwarning("Warnung", "Kein Passwort zum Kopieren vorhanden!")
            
    def add_to_history(self, password):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        strength = self.evaluate_password_strength(password)
        
        entry = {
            "password": password,
            "timestamp": timestamp,
            "length": len(password),
            "strength": strength['text']
        }
        
        self.password_history.append(entry)
        
        # Nur die letzten 50 Passwörter behalten
        if len(self.password_history) > 50:
            self.password_history = self.password_history[-50:]
            
    def generate_multiple(self):
        if not any([self.use_lowercase.get(), self.use_uppercase.get(), 
                   self.use_digits.get(), self.use_special.get()]):
            messagebox.showwarning("Warnung", "Bitte wähle mindestens eine Zeichen-Art aus!")
            return
            
        chars = self.build_character_set()
        length = self.length_var.get()
        
        passwords = []
        for _ in range(5):
            password = self.generate_mixed_password(chars, length)
            passwords.append(password)
            self.add_to_history(password)
            
        # Fenster für Multiple Passwords
        multi_window = tk.Toplevel(self.window)
        multi_window.title("🔢 Generierte Passwörter")
        multi_window.geometry("500x400")
        multi_window.configure(bg="#f0f0f0")
        
        tk.Label(
            multi_window,
            text="🔢 5 generierte Passwörter:",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        # Text-Widget für Passwörter
        text_widget = tk.Text(
            multi_window,
            font=("Courier", 12),
            bg="#ffffff",
            relief=tk.RAISED,
            bd=2
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for i, pwd in enumerate(passwords, 1):
            strength = self.evaluate_password_strength(pwd)
            text_widget.insert(tk.END, f"{i}. {pwd} ({strength['text']})\n\n")
            
        text_widget.config(state=tk.DISABLED)
        
        # Copy All Button
        def copy_all():
            multi_window.clipboard_clear()
            multi_window.clipboard_append('\n'.join(passwords))
            messagebox.showinfo("Kopiert", "Alle Passwörter wurden kopiert!")
            
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
            messagebox.showinfo("Historie", "Noch keine Passwörter in der Historie!")
            return
            
        # Historie-Fenster
        history_window = tk.Toplevel(self.window)
        history_window.title("📜 Passwort-Historie")
        history_window.geometry("700x500")
        history_window.configure(bg="#f0f0f0")
        
        tk.Label(
            history_window,
            text=f"📜 Passwort-Historie ({len(self.password_history)} Einträge):",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        # Treeview für Historie
        columns = ("Zeit", "Passwort", "Länge", "Stärke")
        tree = ttk.Treeview(history_window, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Daten einfügen (neueste zuerst)
        for entry in reversed(self.password_history):
            tree.insert("", 0, values=(
                entry["timestamp"],
                entry["password"],
                entry["length"],
                entry["strength"]
            ))
            
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=10)
        
    def export_passwords(self):
        if not self.password_history:
            messagebox.showinfo("Export", "Keine Passwörter zum Exportieren!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.password_history, f, indent=2, ensure_ascii=False)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("Passwort-Historie\n")
                        f.write("=" * 50 + "\n\n")
                        for entry in self.password_history:
                            f.write(f"Zeit: {entry['timestamp']}\n")
                            f.write(f"Passwort: {entry['password']}\n")
                            f.write(f"Länge: {entry['length']}\n")
                            f.write(f"Stärke: {entry['strength']}\n")
                            f.write("-" * 30 + "\n\n")
                            
                messagebox.showinfo("Export", f"Passwörter erfolgreich exportiert nach:\n{filename}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Export fehlgeschlagen:\n{str(e)}")
                
    def clear_history(self):
        if messagebox.askyesno("Bestätigung", "Möchtest du wirklich die komplette Historie löschen?"):
            self.password_history.clear()
            messagebox.showinfo("Gelöscht", "Historie wurde geleert!")
            
    def save_settings(self):
        settings = {
            "length": self.length_var.get(),
            "use_lowercase": self.use_lowercase.get(),
            "use_uppercase": self.use_uppercase.get(),
            "use_digits": self.use_digits.get(),
            "use_special": self.use_special.get(),
            "exclude_ambiguous": self.exclude_ambiguous.get()
        }
        
        try:
            with open("password_generator_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except:
            pass  # Fehler ignorieren
            
    def load_settings(self):
        try:
            if os.path.exists("password_generator_settings.json"):
                with open("password_generator_settings.json", "r") as f:
                    settings = json.load(f)
                    
                self.length_var.set(settings.get("length", 12))
                self.use_lowercase.set(settings.get("use_lowercase", True))
                self.use_uppercase.set(settings.get("use_uppercase", True))
                self.use_digits.set(settings.get("use_digits", True))
                self.use_special.set(settings.get("use_special", True))
                self.exclude_ambiguous.set(settings.get("exclude_ambiguous", False))
                
                self.update_length_label(str(self.length_var.get()))
        except:
            pass  # Fehler ignorieren, Standardwerte verwenden
            
    def on_closing(self):
        self.save_settings()
        self.window.destroy()
        
    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


# Hauptprogramm
if __name__ == "__main__":
    print("🔐 Passwort Generator wird gestartet...")
    
    try:
        app = PasswordGenerator()
        app.run()
    except Exception as e:
        print(f"Fehler beim Starten: {e}")
        input("Drücke Enter zum Beenden...")