class SimpleChatbot:
    def __init__(self):
        """Initialisiert den Chatbot mit vordefinierten Antworten"""
        self.responses = {
            "hallo": "Hallo! Wie geht es dir? 😊",
            "hi": "Hi! Schön dich zu sehen! 👋",
            "hey": "Hey! Was kann ich für dich tun? 🤖",
            "wie geht's": "Mir geht's gut, danke! Und dir? 😊",
            "wie geht es dir": "Mir geht's super! Ich bin bereit zu helfen! 🚀",
            "gut": "Das freut mich zu hören! 😊",
            "schlecht": "Oh nein, das tut mir leid. Kann ich helfen? 🤗",
            "danke": "Gern geschehen! 😊",
            "dankeschön": "Immer gerne! 🌟",
            "bye": "Auf Wiedersehen! Bis bald! 👋",
            "tschüss": "Tschüss! War schön mit dir zu reden! 😊",
            "auf wiedersehen": "Auf Wiedersehen! Komm gerne wieder! 🚀",
            "hilfe": "Ich kann auf einfache Nachrichten antworten. Probiere: hallo, wie geht's, danke, bye",
            "help": "Ich verstehe: hallo, hi, hey, wie geht's, gut, schlecht, danke, bye, tschüss, hilfe",
            "name": "Ich bin ein einfacher Chatbot! 🤖",
            "wer bist du": "Ich bin dein freundlicher Chatbot-Assistent! 🤖"
        }
    
    def get_response(self, user_input):
        # Eingabe in Kleinbuchstaben umwandeln und Leerzeichen entfernen
        clean_input = user_input.lower().strip()
        
        # Antwort aus Dictionary holen, oder Standard-Antwort
        return self.responses.get(clean_input, "🤔 Das verstehe ich noch nicht. Probiere 'hilfe' für verfügbare Befehle!")
    
    def run(self):
        """Startet den Chatbot im CLI-Modus"""
        print("🤖 Einfacher Chatbot gestartet!")
        print("=" * 40)
        print("💡 Tipp: Schreibe 'hilfe' für verfügbare Befehle")
        print("💡 Beenden mit: quit, exit oder stop")
        print("=" * 40)
        
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
    """Hauptfunktion zum Starten des Chatbots"""
    print("🚀 Schritt 1: Basis CLI-Chatbot")
    print("Entwickelt von: [Dein Name]")
    print()
    
    # Chatbot erstellen und starten
    chatbot = SimpleChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()