import re
import random
from datetime import datetime

class SmartChatbot:
    def __init__(self):
        """Erweitert den einfachen Chatbot um Regex-Pattern-Matching und dynamische Funktionen"""
        # Regex-Patterns mit zugehörigen Funktionen
        self.patterns = {
            # Begrüßung
            r'.*(hallo|hi|hey|guten tag|moin).*': self.greet,
            
            # Verabschiedung
            r'.*(bye|tschüss|auf wiedersehen|ciao).*': self.farewell,
            
            # Zeit/Datum
            r'.*(zeit|uhrzeit|spät|datum|tag|wann).*': self.get_time,
            
            # Name/Info
            r'.*(name|wer bist du|was bist du).*': self.get_name,
            
            # Danke
            r'.*(danke|dankeschön|thanks).*': self.thank_response,
            
            # Einfaches Rechnen (nur Addition/Subtraktion)
            r'.*(\d+)\s*\+\s*(\d+).*': self.add,
            r'.*(\d+)\s*\-\s*(\d+).*': self.subtract,
            
            # Hilfe
            r'.*(hilfe|help|was kannst du).*': self.get_help,
        }
        
        # Vordefinierte Antworten für Variation
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
        
        self.thank_responses = [
            "😊 Gern geschehen!",
            "🌟 Kein Problem!",
            "👍 Immer gerne!"
        ]
    
    def greet(self, match=None):
        """Zufällige Begrüßung"""
        return random.choice(self.greetings)
    
    def farewell(self, match=None):
        """Zufällige Verabschiedung"""
        return random.choice(self.farewells)
    
    def get_time(self, match=None):
        """Aktuelle Zeit und Datum"""
        now = datetime.now()
        return f"🕐 Es ist {now.strftime('%H:%M Uhr')} am {now.strftime('%d.%m.%Y')}"
    
    def get_name(self, match=None):
        """Bot-Information"""
        return "🤖 Ich bin dein Smart Assistant! Ich kann jetzt Zeit sagen und rechnen."
    
    def thank_response(self, match=None):
        """Antwort auf Danke"""
        return random.choice(self.thank_responses)
    
    def add(self, match):
        """Addition zweier Zahlen"""
        num1, num2 = match.groups()
        result = int(num1) + int(num2)
        return f"🔢 {num1} + {num2} = {result}"
    
    def subtract(self, match):
        """Subtraktion zweier Zahlen"""
        num1, num2 = match.groups()
        result = int(num1) - int(num2)
        return f"🔢 {num1} - {num2} = {result}"
    
    def get_help(self, match=None):
        """Hilfe-Information"""
        return """🤖 Das kann ich:
        
🕐 Zeit: 'Wie spät ist es?', 'Welches Datum?'
🔢 Rechnen: '5 + 3', '10 - 2'
💬 Smalltalk: Hallo, Danke, Tschüss
❓ Hilfe: 'Was kannst du?'"""
    
    def get_response(self, user_input):
        """Verarbeitet Benutzereingabe mit Regex-Pattern-Matching"""
        user_input_lower = user_input.lower().strip()
        
        # Durch alle Patterns gehen
        for pattern, response_func in self.patterns.items():
            match = re.search(pattern, user_input_lower)
            if match:
                return response_func(match)
        
        # Fallback-Antworten
        fallback_responses = [
            "🤔 Das verstehe ich noch nicht. Probiere 'hilfe' für verfügbare Funktionen!",
            "❓ Hmm, das kenne ich noch nicht. Frag mich nach Zeit oder lass mich rechnen!",
            "🔍 Interessant! Leider weiß ich dazu nichts. Was anderes?"
        ]
        
        return random.choice(fallback_responses)
    
    def run(self):
        """Startet den erweiterten Chatbot im CLI-Modus"""
        print("🤖 Smart Assistant Chatbot gestartet!")
        print("=" * 50)
        print("💡 Tipp: Schreibe 'hilfe' für alle Funktionen")
        print("💡 Beenden mit: quit, exit oder stop")
        print("=" * 50)
        
        while True:
            try:
                # Benutzereingabe
                user_input = input("\nDu: ").strip()
                
                # Beenden-Befehle
                if user_input.lower() in ['quit', 'exit', 'stop', 'beenden']:
                    print("Bot: Auf Wiedersehen! 👋")
                    break
                
                # Leere Eingabe ignorieren
                if not user_input:
                    continue
                
                # Bot-Antwort
                response = self.get_response(user_input)
                print(f"Bot: {response}")
                
            except KeyboardInterrupt:
                print("\n\nBot: Programm durch Benutzer beendet. Auf Wiedersehen! 👋")
                break
            except Exception as e:
                print(f"Bot: Ein Fehler ist aufgetreten: {e}")


def main():
    """Hauptfunktion zum Starten des erweiterten Chatbots"""
    print("🚀 Schritt 2: Erweiterte CLI mit Regex-Patterns")
    print("Entwickelt von: [Dein Name]")
    print()
    
    # Chatbot erstellen und starten
    chatbot = SmartChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()