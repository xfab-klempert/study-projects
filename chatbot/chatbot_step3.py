import tkinter as tk
import re
import random
from datetime import datetime

class SmartChatbot:
    def __init__(self):
        """Chatbot-Logik aus Schritt 2 + neue Wetter-Simulation"""
        # Erweiterte Regex-Patterns
        self.patterns = {
            # Begrüßung
            r'.*(hallo|hi|hey|guten tag|moin).*': self.greet,
            
            # Verabschiedung  
            r'.*(bye|tschüss|auf wiedersehen|ciao).*': self.farewell,
            
            # Zeit/Datum
            r'.*(zeit|uhrzeit|spät|datum|tag|wann).*': self.get_time,
            
            # NEU: Wetter (simuliert)
            r'.*(wetter|temperatur|warm|kalt|sonne|regen).*': self.get_weather,
            
            # Name/Info
            r'.*(name|wer bist du|was bist du).*': self.get_name,
            
            # Rechnen (erweitert um Multiplikation/Division)
            r'.*(\d+)\s*\+\s*(\d+).*': self.add,
            r'.*(\d+)\s*\-\s*(\d+).*': self.subtract,
            r'.*(\d+)\s*[\*x]\s*(\d+).*': self.multiply,
            r'.*(\d+)\s*[\/\:]\s*(\d+).*': self.divide,
            
            # Danke
            r'.*(danke|dankeschön|thanks).*': self.thank_response,
            
            # Hilfe
            r'.*(hilfe|help|was kannst du).*': self.get_help,
        }
        
        # Vordefinierte Antworten
        self.greetings = [
            "👋 Hallo! Schön dich zu sehen!",
            "🌟 Hi! Wie kann ich dir helfen?",
            "😊 Hey! Was kann ich für dich tun?"
        ]
        
        self.farewells = [
            "👋 Auf Wiedersehen! Bis bald!",
            "🌟 Tschüss! War schön mit dir zu reden!",
            "😊 Bye! Komm gerne wieder!"
        ]
        
        # NEU: Wetter-Antworten
        self.weather_responses = [
            "🌤️ Heute ist es sonnig und 22°C!",
            "🌧️ Es regnet leicht bei 18°C",
            "❄️ Ziemlich kalt heute, nur 5°C",
            "🌈 Wechselhaft, 15°C mit Wolken"
        ]
        
        self.thank_responses = [
            "😊 Gern geschehen!",
            "🌟 Kein Problem!",
            "👍 Immer gerne!"
        ]
    
    def greet(self, match=None):
        return random.choice(self.greetings)
    
    def farewell(self, match=None):
        return random.choice(self.farewells)
    
    def get_time(self, match=None):
        now = datetime.now()
        return f"🕐 Es ist {now.strftime('%H:%M Uhr')} am {now.strftime('%d.%m.%Y')}"
    
    def get_weather(self, match=None):
        """NEU: Simulierte Wetter-Antwort"""
        return random.choice(self.weather_responses)
    
    def get_name(self, match=None):
        return "🤖 Ich bin dein Smart Assistant! Ich kann Zeit sagen, Wetter simulieren und rechnen."
    
    def add(self, match):
        num1, num2 = match.groups()
        result = int(num1) + int(num2)
        return f"🔢 {num1} + {num2} = {result}"
    
    def subtract(self, match):
        num1, num2 = match.groups()
        result = int(num1) - int(num2)
        return f"🔢 {num1} - {num2} = {result}"
    
    def multiply(self, match):
        """NEU: Multiplikation"""
        num1, num2 = match.groups()
        result = int(num1) * int(num2)
        return f"🔢 {num1} × {num2} = {result}"
    
    def divide(self, match):
        """NEU: Division"""
        num1, num2 = match.groups()
        if int(num2) == 0:
            return "❌ Division durch Null ist nicht möglich!"
        result = int(num1) / int(num2)
        return f"🔢 {num1} ÷ {num2} = {result:.2f}"
    
    def thank_response(self, match=None):
        return random.choice(self.thank_responses)
    
    def get_help(self, match=None):
        return """🤖 Das kann ich:
        
🕐 Zeit: 'Wie spät ist es?', 'Welches Datum?'
🌤️ Wetter: 'Wie ist das Wetter?'
🔢 Rechnen: '5 + 3', '10 - 2', '4 * 6', '12 / 3'
💬 Smalltalk: Hallo, Danke, Tschüss
❓ Hilfe: 'Was kannst du?'"""
    
    def get_response(self, user_input):
        user_input_lower = user_input.lower().strip()
        
        # Durch alle Patterns gehen
        for pattern, response_func in self.patterns.items():
            match = re.search(pattern, user_input_lower)
            if match:
                return response_func(match)
        
        # Fallback-Antworten
        fallback_responses = [
            "🤔 Das verstehe ich noch nicht. Frag mich nach Zeit, Wetter oder lass mich rechnen!",
            "❓ Hmm, das kenne ich noch nicht. Probiere 'hilfe' für verfügbare Funktionen!",
            "🔍 Interessant! Leider weiß ich dazu nichts. Was anderes?"
        ]
        
        return random.choice(fallback_responses)


class ChatbotGUI:
    def __init__(self):
        """Erste einfache GUI-Implementierung"""
        self.bot = SmartChatbot()
        self.window = tk.Tk()
        self.window.title("🤖 Smart Assistant Chatbot")
        self.window.geometry("600x500")
        self.window.configure(bg="#f0f0f0")
        
        self.setup_gui()
        
    def setup_gui(self):
        """Einfache GUI mit grundlegenden Elementen"""
        # Titel
        title_label = tk.Label(
            self.window,
            text="🤖 Smart Assistant Chatbot",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2196F3"
        )
        title_label.pack(pady=10)
        
        # Chat-Bereich Frame
        chat_frame = tk.Frame(self.window, bg="#f0f0f0")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Chat-Verlauf (Text-Widget)
        self.chat_area = tk.Text(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#333333",
            relief=tk.RAISED,
            bd=2
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        # Eingabe-Bereich
        input_frame = tk.Frame(self.window, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Eingabefeld
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12),
            relief=tk.RAISED,
            bd=2,
            bg="#ffffff"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        self.input_field.focus()
        
        # Senden-Button
        self.send_button = tk.Button(
            input_frame,
            text="Senden",
            command=self.send_message,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=20
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Willkommensnachricht
        self.add_bot_message("Hallo! 🤖 Ich bin dein Smart Assistant. Frag mich nach Zeit, Wetter oder lass mich rechnen!")
        
    def add_user_message(self, message):
        self.chat_area.insert(tk.END, f"Du: {message}\n")
        self.chat_area.see(tk.END)
        
    def add_bot_message(self, message):
        self.chat_area.insert(tk.END, f"Bot: {message}\n\n")
        self.chat_area.see(tk.END)
        
    def send_message(self, event=None):
        user_input = self.input_field.get().strip()
        if not user_input:
            return
            
        # User-Nachricht hinzufügen
        self.add_user_message(user_input)
        self.input_field.delete(0, tk.END)
        
        # Bot-Antwort generieren und anzeigen
        response = self.bot.get_response(user_input)
        self.add_bot_message(response)
        
    def run(self):
        self.window.mainloop()


# Hauptprogramm
if __name__ == "__main__":
    print("🚀 Schritt 3: Erste GUI-Version mit Tkinter")
    print("Entwickelt von: [Dein Name]")
    print()
    
    try:
        app = ChatbotGUI()
        app.run()
    except Exception as e:
        print(f"Fehler beim Starten: {e}")
        input("Drücke Enter zum Beenden...")