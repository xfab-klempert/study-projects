import random
import string

def generate_password(length=8):
    """Einfacher Passwort-Generator"""
    # Alle verfügbaren Zeichen
    characters = string.ascii_letters + string.digits
    
    # Passwort generieren
    password = ""
    for i in range(length):
        password += random.choice(characters)
    
    return password

def main():
    print("🔐 Einfacher Passwort Generator")
    print("-" * 30)
    
    while True:
        try:
            length = int(input("Passwort-Länge eingeben (oder 0 zum Beenden): "))
            
            if length == 0:
                print("Auf Wiedersehen!")
                break
            elif length < 4:
                print("❌ Passwort muss mindestens 4 Zeichen lang sein!")
            else:
                password = generate_password(length)
                print(f"✅ Dein Passwort: {password}")
                
        except ValueError:
            print("❌ Bitte gib eine gültige Zahl ein!")

if __name__ == "__main__":
    main()