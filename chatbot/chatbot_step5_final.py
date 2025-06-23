import tkinter as tk
from tkinter import scrolledtext
import re
import random
from datetime import datetime
import threading

class SmartChatbot:
    def __init__(self):
        # Erweiterte Patterns mit mehr Funktionen
        self.patterns = {
            # Wetter (ohne API - simuliert)
            r'.*(wetter|temperatur|warm|kalt|sonne|regen).*': self.get_weather,
            
            # Zeit/Datum
            r'.*(zeit|uhrzeit|spät|datum|tag|wann).*': self.get_time,
            
            # Name/Info
            r'.*(name|wer bist du|was bist du).*': self.get_name,
            
            # Rechnen - erweitert
            r'.*rechnen.*(\d+).*(\d+).*': self.calculate_simple,
            r'(\d+\.?\d*)\s*[\+]\s*(\d+\.?\d*)': self.add,
            r'(\d+\.?\d*)\s*[\-]\s*(\d+\.?\d*)': self.subtract,
            r'(\d+\.?\d*)\s*[\*x]\s*(\d+\.?\d*)': self.multiply,
            r'(\d+\.?\d*)\s*[\/\:]\s*(\d+\.?\d*)': self.divide,
            
            # Begrüßung
            r'.*(hallo|hi|hey|guten tag|moin).*': self.greet,
            
            # Verabschiedung
            r'.*(bye|tschüss|auf wiedersehen|ciao).*': self.farewell,
            
            # Danke
            r'.*(danke|dankeschön|thanks).*': self.thank_response,
            
            # Witze (ohne API - vordefiniert)
            r'.*(witz|lustig|lachen|joke|humor).*': self.get_joke,
            
            # Hilfe
            r'.*(hilfe|help|was kannst du|funktionen).*': self.get_help,
            
            # Würfel
            r'.*(würfel|dice|zufallszahl|random).*': self.roll_dice,
            
            # Wochentag
            r'.*(wochentag|welcher tag).*': self.get_weekday,
        }
        
        # Vordefinierte Antworten
        self.weather_responses = [
            "🌤️ Heute ist es sonnig und 22°C!",
            "🌧️ Es regnet leicht bei 18°C",
            "❄️ Ziemlich kalt heute, nur 5°C",
            "🌈 Wechselhaft, 15°C mit Wolken",
            "☀️ Strahlender Sonnenschein, 25°C!"
        ]
        
        self.jokes = [
            "Warum nehmen Geister keinen Aufzug? Sie haben Angst vor Buh-Geistern! 👻",
            "Was ist grün und klopft an der Tür? Ein Klopfsalat! 🥗",
            "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann! 👻",
            "Was sagt ein großer Stift zum kleinen Stift? Wachs-mal-stift! ✏️",
            "Warum programmieren Java-Entwickler Brillen? Weil sie nicht C# können! 🤓",
            "Was ist der Unterschied zwischen einem Informatiker und einem normalen Menschen? Der Informatiker denkt, dass 31. Oktober und 25. Dezember derselbe Tag sind!"
        ]
    
    def get_weather(self, match=None):
        return random.choice(self.weather_responses)
    
    def get_time(self, match=None):
        now = datetime.now()
        return f"🕐 Es ist {now.strftime('%H:%M Uhr')} am {now.strftime('%d.%m.%Y')}"
    
    def get_name(self, match=None):
        return "🤖 Ich bin dein persönlicher Smart Assistant! Ich kann rechnen, Witze erzählen und dir helfen."
    
    def calculate_simple(self, match):
        num1, num2 = match.groups()
        result = int(num1) + int(num2)
        return f"🔢 {num1} + {num2} = {result}"
    
    def add(self, match):
        num1, num2 = match.groups()
        result = float(num1) + float(num2)
        return f"🔢 {num1} + {num2} = {result}"
    
    def subtract(self, match):
        num1, num2 = match.groups()
        result = float(num1) - float(num2)
        return f"🔢 {num1} - {num2} = {result}"
    
    def multiply(self, match):
        num1, num2 = match.groups()
        result = float(num1) * float(num2)
        return f"🔢 {num1} × {num2} = {result}"
    
    def divide(self, match):
        num1, num2 = match.groups()
        if float(num2) == 0:
            return "❌ Division durch Null ist nicht möglich!"
        result = float(num1) / float(num2)
        return f"🔢 {num1} ÷ {num2} = {result:.2f}"
    
    def greet(self, match=None):
        greetings = [
            "👋 Hallo! Schön dich zu sehen!",
            "🌟 Hi! Wie kann ich dir helfen?",
            "😊 Hey! Was kann ich für dich tun?",
            "🚀 Hallo! Bereit für interessante Gespräche?"
        ]
        return random.choice(greetings)
    
    def farewell(self, match=None):
        farewells = [
            "👋 Auf Wiedersehen! Bis bald!",
            "🌟 Tschüss! War schön mit dir zu reden!",
            "😊 Bye! Komm gerne wieder!",
            "🚀 Ciao! Bis zum nächsten Mal!"
        ]
        return random.choice(farewells)
    
    def thank_response(self, match=None):
        responses = [
            "😊 Gern geschehen!",
            "🌟 Kein Problem!",
            "👍 Immer gerne!",
            "🚀 Freut mich, dass ich helfen konnte!"
        ]
        return random.choice(responses)
    
    def get_joke(self, match=None):
        return f"😂 {random.choice(self.jokes)}"
    
    def get_help(self, match=None):
        return """🤖 Das kann ich alles:
        
✨ Rechnen: '5 + 3', '10 - 2', '4 * 6', '15 / 3'
🌤️ Wetter: 'Wie ist das Wetter?'
🕐 Zeit: 'Wie spät ist es?'
😂 Witze: 'Erzähl einen Witz'
🎲 Würfeln: 'Würfel eine Zahl'
📅 Wochentag: 'Welcher Tag ist heute?'
💬 Smalltalk: Hallo, Danke, Tschüss"""
    
    def roll_dice(self, match=None):
        number = random.randint(1, 6)
        return f"🎲 Gewürfelt: {number}"
    
    def get_weekday(self, match=None):
        weekdays = {
            0: "Montag", 1: "Dienstag", 2: "Mittwoch", 
            3: "Donnerstag", 4: "Freitag", 5: "Samstag", 6: "Sonntag"
        }
        today = datetime.now().weekday()
        return f"📅 Heute ist {weekdays[today]}"
    
    def get_response(self, user_input):
        user_input_lower = user_input.lower().strip()
        
        # Durch alle Patterns gehen
        for pattern, response_func in self.patterns.items():
            match = re.search(pattern, user_input_lower)
            if match:
                if callable(response_func):
                    return response_func(match)
                else:
                    return response_func
        
        # Fallback-Antworten
        fallback_responses = [
            "🤔 Das verstehe ich noch nicht. Frag mich nach Wetter, Zeit, Witzen oder lass mich rechnen!",
            "❓ Hmm, das kenne ich noch nicht. Probiere 'Hilfe' für verfügbare Funktionen!",
            "🔍 Interessant! Leider weiß ich dazu nichts. Was anderes?",
            "💭 Das ist neu für mich. Kannst du es anders formulieren?"
        ]
        
        return random.choice(fallback_responses)


class ChatbotGUI:
    def __init__(self):
        self.bot = SmartChatbot()
        self.window = tk.Tk()
        self.window.title("🤖 Smart Assistant Chatbot")
        self.window.geometry("700x600")
        self.window.configure(bg="#f0f0f0")
        
        self.setup_gui()
        
    def setup_gui(self):
        # Header
        header_frame = tk.Frame(self.window, bg="#2196F3", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🤖 Smart Assistant Chatbot",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Chat-Bereich
        chat_frame = tk.Frame(self.window, bg="#f0f0f0")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat-Verlauf
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#333333",
            relief=tk.RAISED,
            bd=2
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        # Eingabe-Bereich
        input_frame = tk.Frame(self.window, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Eingabefeld
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12),
            relief=tk.RAISED,
            bd=2,
            bg="#ffffff"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)
        self.input_field.focus()
        
        # Button-Frame
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.pack(side=tk.RIGHT)
        
        # Senden-Button
        self.send_button = tk.Button(
            button_frame,
            text="Senden",
            command=self.send_message,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Hilfe-Button
        help_button = tk.Button(
            button_frame,
            text="Hilfe",
            command=self.show_help,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        help_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Clear-Button
        clear_button = tk.Button(
            button_frame,
            text="Löschen",
            command=self.clear_chat,
            bg="#f44336",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15
        )
        clear_button.pack(side=tk.LEFT)
        
        # Willkommensnachricht
        self.add_bot_message("Hallo! 🤖 Ich bin dein Smart Assistant. Frag mich nach Wetter, Zeit, lass mich rechnen oder erzähl mir einen Witz! Schreib 'help' für alle Funktionen.")
        
    def add_message(self, sender, message, color="#333333"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Message formatieren
        formatted_message = f"[{timestamp}] {sender}: {message}\n"
        
        # Text einfügen
        self.chat_area.insert(tk.END, formatted_message)
        
        # Farbe anwenden (nur für letzte Nachricht)
        start_line = self.chat_area.index(tk.END + "-2l linestart")
        end_line = self.chat_area.index(tk.END + "-1l lineend")
        
        # Scroll zum Ende
        self.chat_area.see(tk.END)
        
    def add_user_message(self, message):
        self.add_message("Du", message, "#1976D2")
        
    def add_bot_message(self, message):
        self.add_message("Bot", message, "#388E3C")
        
    def send_message(self, event=None):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
            
        # User-Nachricht hinzufügen
        self.add_user_message(user_input)
        self.input_field.delete(0, tk.END)
        
        # Bot-Antwort in separatem Thread
        threading.Thread(target=self.process_bot_response, args=(user_input,), daemon=True).start()
        
    def process_bot_response(self, user_input):
        try:
            # Bot-Antwort generieren
            response = self.bot.get_response(user_input)
            
            # GUI-Update im Main-Thread
            self.window.after(0, lambda: self.add_bot_message(response))
            
        except Exception as e:
            error_msg = f"Fehler: {str(e)}"
            self.window.after(0, lambda: self.add_bot_message(error_msg))
            
    def show_help(self):
        help_response = self.bot.get_help()
        self.add_bot_message(help_response)
        
    def clear_chat(self):
        self.chat_area.delete(1.0, tk.END)
        self.add_bot_message("Chat wurde geleert! 🧹 Wie kann ich dir helfen?")
        
    def run(self):
        self.window.mainloop()


# Hauptprogramm
if __name__ == "__main__":
    print("🤖 Smart Assistant Chatbot wird gestartet...")
    
    try:
        app = ChatbotGUI()
        app.run()
    except Exception as e:
        print(f"Fehler beim Starten: {e}")
        input("Drücke Enter zum Beenden...")