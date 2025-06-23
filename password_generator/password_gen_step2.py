import random
import string

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase  
        self.digits = string.digits
        self.special_chars = "!@#$%&*+-=?"
    
    def generate_password(self, length, use_upper=True, use_digits=True, use_special=False):
        """Erweiterte Passwort-Generierung mit Optionen"""
        characters = self.lowercase  # Kleinbuchstaben immer dabei
        
        if use_upper:
            characters += self.uppercase
        if use_digits:
            characters += self.digits
        if use_special:
            characters += self.special_chars
        
        # Passwort generieren
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    def check_password_strength(self, password):
        """Einfache Passwort-Stärke Bewertung"""
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
            return "🟢 Stark"
        elif score >= 3:
            return "🟡 Mittel"
        else:
            return "🔴 Schwach"

def main():
    generator = PasswordGenerator()
    
    print("🔐 Erweiterte Passwort Generator")
    print("=" * 35)
    
    while True:
        print("\nOptionen:")
        print("1. Passwort generieren")
        print("2. Passwort bewerten")
        print("0. Beenden")
        
        choice = input("\nWähle eine Option: ")
        
        if choice == "0":
            print("Auf Wiedersehen!")
            break
            
        elif choice == "1":
            try:
                length = int(input("Länge (4-50): "))
                if length < 4 or length > 50:
                    print("❌ Länge muss zwischen 4 und 50 sein!")
                    continue
                
                use_upper = input("Großbuchstaben? (j/n): ").lower() == 'j'
                use_digits = input("Zahlen? (j/n): ").lower() == 'j'
                use_special = input("Sonderzeichen? (j/n): ").lower() == 'j'
                
                password = generator.generate_password(length, use_upper, use_digits, use_special)
                strength = generator.check_password_strength(password)
                
                print(f"\n✅ Passwort: {password}")
                print(f"💪 Stärke: {strength}")
                
            except ValueError:
                print("❌ Ungültige Eingabe!")
                
        elif choice == "2":
            password = input("Passwort zum Bewerten eingeben: ")
            strength = generator.check_password_strength(password)
            print(f"💪 Stärke: {strength}")
            
        else:
            print("❌ Ungültige Option!")

if __name__ == "__main__":
    main()