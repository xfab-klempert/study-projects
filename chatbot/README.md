# 📋 **Projekt Ablaufplan: Chatbot-Entwicklung**

## 📚 **Zusätzliche Ressourcen:**

- **Interaktive Python Lernplatform:** https://www.w3schools.com/python/
- **Python Dokumentation:** https://docs.python.org/3/
- **tkinter Tutorial:** https://guipy.de/doku.php?id=de:tkinter
- **Regex Tutorial:** https://regexr.com/
- **Threading in Python:** https://docs.python.org/3/library/threading.html

**Viel Erfolg bei der Umsetzung! 🚀**

---

## 🎯 **Nach jedem Schritt:**

### **Checkpoint-Aufgaben:**
- [ ] Kurze Reflexion: Was lief gut? Was war schwierig?
- [ ] Regex-Patterns verstehen und dokumentieren
- [ ] GUI-Komponenten testen und verstehen
- [ ] Threading-Konzepte durchgehen
- [ ] Funktionalität mit verschiedenen Eingaben testen

### **Debugging-Tipps:**
- [ ] `print()` Statements für Debugging nutzen
- [ ] Regex-Patterns online testen (regexr.com)
- [ ] GUI-Komponenten schrittweise hinzufügen
- [ ] Threading-Probleme mit `.after()` lösen

---

## 🚀 **Schritt 1: CLI-Grundlagen & Dictionary-basierte Antworten**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Einfacher Dictionary-basierter Chatbot über Terminal
  - [ ] Vordefinierte Antworten für häufige Begriffe
  - [ ] Eingabe-Normalisierung (lowercase, strip)
  - [ ] Beenden-Option (quit, exit, stop)
- [ ] While-Loop für kontinuierliche Unterhaltung
- [ ] Fallback-Antwort für unbekannte Eingaben
- [ ] Einfache Hilfe-Funktion
- [ ] Fehlerbehandlung bei Eingabe-Problemen

### **💡 Kurz erklärt (ohne Code):**
- **Dictionary-basierter Chatbot:** Der Bot nutzt eine feste Liste von Frage-Antwort-Paaren.
  - Beispiel: Bei „hallo" antwortet er immer „Hallo, wie kann ich helfen?".
- **Eingabe-Normalisierung:** Nutzer-Eingaben werden vereinheitlicht, damit ähnliche Eingaben gleich erkannt werden.
  - Beispiel: „  HALLO  " wird intern wie „hallo" behandelt.
- **Fallback-Antwort:** Wenn nichts passt, gibt es trotzdem eine sinnvolle Antwort.
  - Beispiel: „Dazu habe ich noch keine Antwort, versuch bitte ein anderes Wort.".
- **Hilfe-Funktion:** Der Bot erklärt kurz, welche Eingaben er versteht.
  - Beispiel: „Du kannst Begriffe wie hallo, hilfe oder zeit nutzen.".

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Grundlegende Syntax:**
  - `print()` - Ausgabe
  - `input()` - Eingabe
  - `len()` - String-Länge
  - `dict{}` - Dictionary
- **String Operations:**
  - `.lower()` - Kleinschreibung
  - `.strip()` - Leerzeichen entfernen
  - `in` Operator für Dictionary-Keys
- **Control Flow:**
  - `while` Loop
  - `if/elif/else` Bedingungen
  - `break` Statement
- **Error Handling:**
  - `try/except` Blöcke
  - `KeyboardInterrupt` Exception
- **Funktionen:**
  - `def` Function Definition
  - `return` Statement

### **Vorbereitung & Setup:**
- [ ] Python-Entwicklungsumgebung einrichten (VS Code/PyCharm)

### **Praktische Aufgaben:**
1. [ ] **`chatbot_step1.py` implementieren:**
   - `SimpleChatbot` Klasse schreiben
   - Dictionary mit Antwort-Paaren erstellen
   - `get_response()` Methode implementieren
   - While-Loop für Chat-Schleife
   - Try/Except für Eingabe-Validierung

2. [ ] **Testing:**
   - Verschiedene Eingaben testen
   - Edge-Cases testen (leere Eingabe, Sonderzeichen)

<br/>

## 🔧 **Schritt 2: Erweiterte CLI mit Regex-Pattern-Matching**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] SmartChatbot-Klasse mit Regex-Pattern-System
- [ ] Dynamische Zeit- und Datumsabfrage
- [ ] Einfache Rechenoperationen (Addition, Subtraktion)
- [ ] Verschiedene Begrüßungs- und Verabschiedungsvarianten
- [ ] Zufällige Antwort-Auswahl für natürlichere Gespräche
- [ ] Pattern-basierte Eingabe-Erkennung
- [ ] Erweiterte Hilfe-Funktion mit Funktionsübersicht

### **💡 Kurz erklärt (ohne Code):**
- **Pattern-Erkennung mit Regex:** Der Bot erkennt Satzmuster statt nur exakter Wörter.
  - Beispiel: „Wie spät ist es?" und „Kannst du mir die Uhrzeit sagen?" führen zur gleichen Funktion.
- **Dynamische Zeit/Datum-Ausgabe:** Die Antwort wird beim Fragen neu erzeugt.
  - Beispiel: Morgens zeigt der Bot eine andere Uhrzeit als abends.
- **Einfache Rechenoperationen:** Zahlen werden aus der Eingabe gelesen und berechnet.
  - Beispiel: „Rechne 7 + 5" gibt „12" zurück.
- **Zufällige Antworten:** Es gibt mehrere passende Antworten, damit der Chat natürlicher wirkt.
  - Beispiel: Auf „hallo" kommen abwechselnd verschiedene Begrüßungen.

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Regex Operations:**
  - `re` Module
  - `re.search()` Function
  - `match.groups()` Method
  - Raw Strings `r"pattern"`
- **Advanced Data Structures:**
  - Dictionary mit Funktions-Referenzen
  - `random.choice()` für zufällige Auswahl
  - List Comprehensions
- **Date/Time:**
  - `datetime` Module
  - `datetime.now()`
  - `.strftime()` Formatting
- **Mathematical Operations:**
  - `int()` Type Conversion
  - Basic Math Operations
- **Function References:**
  - Functions as Variables
  - `callable()` Function

### **Praktische Aufgaben:**
1. [ ] **`chatbot_step2.py` implementieren:**
   - `SmartChatbot` Klasse erstellen
   - Regex-Pattern Dictionary aufbauen
   - Verschiedene Response-Funktionen implementieren
   - Zeit- und Datums-Funktionalität
   - Einfache Rechenfunktionen

2. [ ] **Regex-Patterns:**
   - Pattern für Begrüßungen verstehen
   - Zahlen-Extraktion für Rechnen
   - Fallback-System implementieren

<br/>

## 🖥️ **Schritt 3: Erste GUI-Version mit erweiterten Features**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Hauptfenster mit Titel und fester Größe
- [ ] Chatbot-Logik aus Schritt 2 + Wetter-Simulation
- [ ] Chat-Verlauf Anzeige (Text-Widget)
- [ ] Eingabefeld mit Enter-Taste Unterstützung
- [ ] "Senden" Button für Nachrichten
- [ ] Erweiterte Rechenfunktionen (Multiplikation, Division)
- [ ] Wetter-Simulation mit zufälligen Antworten
- [ ] Basis-Styling (Farben, Schriftarten)

### **💡 Kurz erklärt (ohne Code):**
- **Chat-Verlauf:** Alle Nachrichten bleiben sichtbar, nicht nur die letzte.
  - Beispiel: Man sieht oben die erste Frage und unten die aktuelle Antwort.
- **Enter-Taste + Senden-Button:** Beide Wege lösen die gleiche Aktion aus.
  - Beispiel: Nutzer kann Nachricht per Tastatur oder Mausklick senden.
- **Wetter-Simulation:** Der Bot tut so, als gäbe es Wetterdaten.
  - Beispiel: Auf „Wie ist das Wetter?" kommt „Heute sonnig bei 22 Grad" (simuliert).
- **Basis-Styling:** Lesbarkeit und Übersicht werden verbessert.
  - Beispiel: Eigene Farbe für Bot-Text und größere Schrift für Eingaben.

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **tkinter Basics:**
  - `tkinter as tk`
  - `tk.Tk()` - Main Window
  - `tk.Label()` - Text Display
  - `tk.Entry()` - Input Field
  - `tk.Button()` - Clickable Button
  - `tk.Text()` - Multi-line Text Display
- **Layout:**
  - `.pack()` Method
  - `side`, `fill`, `expand` Parameters
  - `padx`, `pady` Spacing
  - `tk.Frame()` - Container
- **Text Widget:**
  - `.insert()` Method
  - `tk.END` Constant
  - `.see()` for Auto-scroll
- **Events:**
  - `command=` Parameter
  - `bind()` Method for Key Events
  - `<Return>` Event
- **Advanced Math:**
  - Division by Zero Handling
  - Float Operations

### **Praktische Aufgaben:**
1. [ ] **`chatbot_step3.py` implementieren:**
   - Hauptfenster mit `tk.Tk()` erstellen
   - Chat-Bereich mit `tk.Text()` Widget
   - Eingabefeld mit Enter-Binding
   - Senden-Button implementieren
   - Wetter-Simulation hinzufügen

2. [ ] **GUI-Event-Handling:**
   - Button-Click Funktion `send_message()`
   - Enter-Taste für Nachrichten senden
   - Chat-Verlauf automatisch scrollen

<br/>

## 🎨 **Schritt 4: Verbessertes Design & Zusatzfunktionen**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Farbiger Header-Bereich (blau)
- [ ] ScrolledText Widget für bessere Chat-Anzeige
- [ ] Mehrere Buttons (Senden, Hilfe, Löschen)
- [ ] Zeitstempel für alle Nachrichten
- [ ] Witze-Sammlung mit zufälliger Auswahl
- [ ] Würfel-Funktion (1-6 Zufallszahl)
- [ ] Dezimalzahlen-Unterstützung beim Rechnen
- [ ] Verbesserte Farbgebung (grün, orange, rot für Buttons)
- [ ] Extra Leerzeilen nach Bot-Nachrichten

### **💡 Kurz erklärt (ohne Code):**
- **ScrolledText:** Der Chatbereich bekommt automatisch eine Scroll-Leiste.
  - Beispiel: Bei langen Chats kann man nach oben zu alten Nachrichten scrollen.
- **Zeitstempel:** Jede Nachricht zeigt, wann sie gesendet wurde.
  - Beispiel: „[14:35] Bot: Hallo!".
- **Würfel-Funktion:** Der Bot kann eine Zufallszahl von 1 bis 6 erzeugen.
  - Beispiel: „Würfle" ergibt „Du hast eine 4 gewürfelt.".
- **Dezimalzahlen:** Rechnen funktioniert auch mit Kommazahlen.
  - Beispiel: „2.5 * 4" ergibt „10.0".

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Advanced Widgets:**
  - `tkinter.scrolledtext`
  - `scrolledtext.ScrolledText()`
  - `tk.Frame()` - Container
- **Layout Management:**
  - Multiple Frames
  - `fill=tk.X`, `fill=tk.BOTH`
  - `expand=True`
  - `pack_propagate(False)`
- **Styling:**
  - `bg=` Background Color
  - `fg=` Foreground Color
  - `font=` Font Tuples
  - `relief=`, `bd=` Border Effects
- **Advanced Functions:**
  - `random.randint()` für Würfel
  - `float()` für Dezimilzahlen
  - String Formatting mit f-strings
- **Time Operations:**
  - Zeitstempel Formatierung
  - `.strftime()` mit verschiedenen Formaten

### **Praktische Aufgaben:**
1. [ ] **`chatbot_step4.py` implementieren:**
   - Header-Frame mit blauem Hintergrund
   - ScrolledText für Chat-Bereich
   - Button-Frame für mehrere Buttons
   - Zeitstempel-Funktionalität
   - Witze- und Würfel-Features

2. [ ] **Advanced GUI Features:**
   - `scrolledtext.ScrolledText` verstehen
   - Multiple Button Layout
   - Chat-Nachrichten mit Zeitstempel
   - Clear-Chat Funktionalität

<br/>

## 📊 **Schritt 5: Threading & Erweiterte Features**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Threading für bessere GUI-Performance
- [ ] Erweiterte Passwort-Stärke Bewertung
- [ ] Wochentag-Abfrage Funktion
- [ ] Erweiterte Witze-Sammlung
- [ ] Garantierter Zeichen-Mix bei komplexeren Antworten
- [ ] Professionelle Farbkodierung für Nachrichten
- [ ] Verbesserte Fehlerbehandlung mit Threading
- [ ] Graceful Error Recovery
- [ ] Optimierte Bot-Response-Verarbeitung

### **💡 Kurz erklärt (ohne Code):**
- **Threading für GUI:** Aufwendige Bot-Antworten laufen im Hintergrund, die Oberfläche bleibt bedienbar.
  - Beispiel: Während der Bot „denkt", kann der Nutzer weiter tippen.
- **Graceful Error Recovery:** Fehler brechen die App nicht sofort ab.
  - Beispiel: Bei ungültiger Eingabe zeigt die App eine Meldung und läuft weiter.
- **Wochentag-Abfrage:** Der Bot kann aus dem aktuellen Datum den Tag nennen.
  - Beispiel: „Welcher Wochentag ist heute?" -> „Heute ist Donnerstag.".
- **Farbkodierung:** Unterschiedliche Nachrichtentypen sind visuell schneller erkennbar.
  - Beispiel: Info grün, Warnung orange, Fehler rot.

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Threading:**
  - `threading` Module
  - `threading.Thread()`
  - `daemon=True`
  - `.after()` Method for GUI Updates
- **Advanced Date Operations:**
  - `datetime.weekday()`
  - Weekday Name Mapping
- **Advanced Algorithms:**
  - `random.shuffle()` für Antwort-Variation
  - `set()` for Unique Elements
  - Complex List Comprehensions
- **GUI Threading:**
  - Main Thread vs Worker Thread
  - `.after()` for Safe GUI Updates
  - Thread-Safe Operations
- **Error Handling:**
  - Multiple Exception Types
  - `try/except/finally`
  - Threading Exception Handling
- **Performance:**
  - Non-blocking GUI Operations
  - Responsive User Interface

### **Praktische Aufgaben:**
1. [ ] **Threading implementieren:**
   - `process_bot_response()` in separatem Thread
   - `.after()` für GUI-Updates
   - Thread-sichere Bot-Antwort-Verarbeitung
   - Performance-Optimierung

2. [ ] **Erweiterte Features:**
   - Wochentag-Funktionalität
   - Erweiterte Witze-Sammlung
   - Verbesserte Fehlerbehandlung
   - Thread-basierte Response-Verarbeitung

<br/>

## 🚀 **Schritt 6: Professionelle Features & Finale Version**

### **🔧 Zusätzliche Erweiterungsmöglichkeiten (Optional):**
- **File I/O:**
  - Chat-Historie speichern/laden (JSON-Datei)
  - Benutzer-Einstellungen persistent speichern
  - Export-Funktion für Chat-Verlauf
- **Advanced Features:**
  - Benutzer-Profile und -Namen
  - Chatbot-Persönlichkeiten
  - Plugin-System für neue Funktionen
- **API Integration:**
  - Echte Wetter-API Anbindung
  - Online-Witze API
  - News-API für aktuelle Nachrichten

### **Praktische Aufgaben:**
1. [ ] **Finale Version testen:**
   - Alle Funktionen durchgehen
   - Performance testen
   - Edge-Cases überprüfen
   - Threading-Stabilität testen

2. [ ] **Optionale Erweiterungen:**
   - Chat-Historie speichern
   - Einstellungen-System
   - Zusätzliche APIs integrieren

---

## 📝 **Abschluss & Präsentation (optional)**

### **Aufgaben:**
- [ ] **Demo vorbereiten:**
  - 5-Minuten Präsentation der Anwendung
  - Vorher/Nachher Vergleich (Schritt 1 vs. Schritt 5)
  - Regex-Pattern Erklärung
  - Threading-Benefits demonstrieren

- [ ] **Code-Review:**
  - Wichtigste Lerninhalte zusammenfassen
  - Regex vs Dictionary Ansatz vergleichen
  - GUI vs CLI Entwicklung diskutieren
  - Threading Best Practices besprechen

- [ ] **Erweiterungsideen diskutieren:**
  - KI/ML Integration Möglichkeiten
  - Web-Interface mit Flask
  - Mobile App Entwicklung
  - Chatbot-Training mit eigenen Daten