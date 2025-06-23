# 📋 **Projekt Ablaufplan: Passwort-Generator**

## 📚 **Zusätzliche Ressourcen:**

- **Interaktive Python Lernplatform:** https://www.w3schools.com/python/
- **Python Dokumentation:** https://docs.python.org/3/
- **tkinter Tutorial:** https://guipy.de/doku.php?id=de:tkinter

**Viel Erfolg bei der Umsetzung! 🚀**

---

## 🎯 **Nach jedem Schritt:**

### **Checkpoint-Aufgaben:**
- [ ] Kurze Reflexion: Was lief gut? Was war schwierig?
- [ ] Fragen für nächsten Schritt notieren
- [ ] Arbeitsstand dokumentieren
- [ ] Funktionalität testen

### **Debugging-Tipps:**
- [ ] `print()` Statements für Debugging nutzen

---

## 🚀 **Schritt 1: CLI-Grundlagen & Python-Basics**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Einfache Passwort-Generierung mit vorgegebener Länge über Terminal
  - [ ] Eingabe-Validierung (mindestens 4 Zeichen)
  - [ ] Beenden-Option (0 eingeben)
- [ ] Verwendung von Buchstaben und Zahlen
- [ ] While-Loop für mehrfache Verwendung
- [ ] Fehlerbehandlung bei ungültiger Eingabe

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Grundlegende Syntax:**
  - `print()` - Ausgabe
  - `input()` - Eingabe
  - `len()` - String-Länge
- **Control Flow:**
  - `while` Loop
  - `if/elif/else` Bedingungen
  - `for` Loop
- **Error Handling:**
  - `try/except` Blöcke
  - `ValueError` Exception
- **String & Random:**
  - `string.ascii_letters`
  - `string.digits`
  - `random.choice()`
- **Funktionen:**
  - `def` Function Definition
  - `return` Statement

### **Vorbereitung & Setup:**
- [ ] Python-Entwicklungsumgebung einrichten (VS Code/PyCharm)

### **Praktische Aufgaben:**
1. [ ] **`password_gen_step1.py` implementieren:**
   - Funktion `generate_password(length)` schreiben
   - Einfache CLI mit `input()` und `print()`
   - While-Loop für Wiederholungen
   - Try/Except für Eingabe-Validierung

2. [ ] **Testing:**
   - Passwörter mit verschiedenen Längen testen
   - Edge-Cases testen (Länge 0, negative Zahlen)

<br/>

## 🔧 **Schritt 2: Erweiterte CLI mit Klassen**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] PasswordGenerator-Klasse erstellen
- [ ] Verschiedene Zeichen-Sets (Kleinbuchstaben, Großbuchstaben, Zahlen, Sonderzeichen)
- [ ] Optionen für jeden Zeichen-Typ (ja/nein Abfrage)
- [ ] Menü-System mit Nummern-Navigation
- [ ] Passwort-Stärke Bewertungsystem
- [ ] Option zum Bewerten existierender Passwörter
- [ ] Erweiterte Längen-Validierung (4-50 Zeichen)

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Objektorientierung:**
  - `class` Definition
  - `__init__()` Konstruktor
  - `self` Parameter
  - Instance Variables
  - Methods vs Functions
- **String Operations:**
  - `string.ascii_lowercase`
  - `string.ascii_uppercase`
  - `string.digits`
  - `.islower()`, `.isupper()`, `.isdigit()`
- **Advanced Functions:**
  - `any()` Function
  - List Comprehensions
  - `''.join()` Method
- **Boolean Logic:**
  - Boolean Variables
  - Logical Operators (`and`, `or`, `not`)

### **Praktische Aufgaben:**
1. [ ] **`password_gen_step2.py` implementieren:**
   - `PasswordGenerator` Klasse erstellen
   - Verschiedene Zeichen-Sets als Klassen-Attribute
   - Methode `generate_password()` mit Parametern
   - Menü-System für Benutzerinteraktion
   - Passwort-Stärke Bewertung implementieren

2. [ ] **Erweiterte Features:**
   - Boolean-Parameter für Zeichen-Arten
   - Passwort-Stärke Algorithmus verstehen
   - Menü-Navigation mit Zahlen-Eingabe

<br/>

## 🖥️ **Schritt 3: Erste GUI-Version**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Hauptfenster mit Titel und fester Größe
- [ ] Eingabefeld für Passwort-Länge
- [ ] 3 Checkboxen (Großbuchstaben, Zahlen, Sonderzeichen)
- [ ] "Passwort generieren" Button
- [ ] Passwort-Anzeige Feld (readonly)
- [ ] "Kopieren" Button für Zwischenablage
- [ ] Eingabe-Validierung mit Popup-Fenstern
- [ ] Basis-Styling (Farben, Schriftarten)

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **tkinter Basics:**
  - `tkinter as tk`
  - `tk.Tk()` - Main Window
  - `tk.Label()` - Text Display
  - `tk.Entry()` - Input Field
  - `tk.Button()` - Clickable Button
  - `tk.Checkbutton()` - Checkbox
- **Layout:**
  - `.pack()` Method
  - `side`, `fill`, `expand` Parameters
  - `padx`, `pady` Spacing
- **Variables:**
  - `tk.StringVar()`
  - `tk.BooleanVar()`
  - `tk.IntVar()`
- **Events:**
  - `command=` Parameter
  - Button Click Events
- **MessageBox:**
  - `tkinter.messagebox`
  - `showinfo()`, `showwarning()`, `showerror()`
- **Clipboard:**
  - `.clipboard_clear()`
  - `.clipboard_append()`

### **Praktische Aufgaben:**
1. [ ] **`password_gen_step3.py` implementieren:**
   - Hauptfenster mit `tk.Tk()` erstellen
   - Titel und Größe setzen
   - Entry-Widget für Passwort-Länge
   - Checkboxen für Optionen (`tk.Checkbutton`)
   - Generate-Button implementieren
   - Passwort-Anzeige mit readonly Entry

2. [ ] **Event-Handling:**
   - Button-Click Funktion `generate_password()`
   - Eingabe-Validierung mit `messagebox`
   - Zwischenablage-Funktionalität

<br/>

## 🎨 **Schritt 4: Verbessertes Design & Schieberegler**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Farbiger Header-Bereich (blau)
- [ ] LabelFrame für Sektionen-Gruppierung
- [ ] Schieberegler (Scale) für Passwort-Länge (4-32)
- [ ] Dynamisches Label zeigt aktuelle Länge
- [ ] Verbesserte Farbgebung (grün, orange, rot für Buttons)
- [ ] Emoji-Icons in Button-Texten
- [ ] Passwort-Stärke Anzeige mit Farb-Coding
- [ ] Professionelleres Layout mit mehreren Frames
- [ ] Verbessertes Eingabefeld-Design

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Advanced Widgets:**
  - `tk.Frame()` - Container
  - `tk.LabelFrame()` - Grouped Container
  - `tk.Scale()` - Slider Widget
- **Layout Parameters:**
  - `fill=tk.X`, `fill=tk.BOTH`
  - `expand=True`
  - `pack_propagate(False)`
- **Styling:**
  - `bg=` Background Color
  - `fg=` Foreground Color
  - `font=` Font Tuples
  - `relief=`, `bd=` Border Effects
- **Callbacks:**
  - `command=` with Parameters
  - `configure()` Method
  - Dynamic Label Updates
- **Color Systems:**
  - Hex Color Codes (#RRGGBB)
  - Named Colors

### **Praktische Aufgaben:**
1. [ ] **`password_gen_step4.py` implementieren:**
   - Header-Frame mit blauem Hintergrund
   - LabelFrame für Sektionen
   - Scale-Widget (Schieberegler) für Länge
   - Verbesserte Farbgebung
   - Icons in Button-Texten (Emojis)

2. [ ] **Advanced Widgets:**
   - `tk.Scale` für Passwort-Länge
   - Callback-Funktionen (`command=self.update_length_label`)
   - `tk.StringVar()` für dynamische Texte
   - Layout mit mehreren Frames

<br/>

## 📊 **Schritt 5: Historie & Multiple Passwörter**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Passwort-Historie Liste im Hintergrund
- [ ] "5 Passwörter generieren" Button
- [ ] "Historie anzeigen" Button
- [ ] Popup-Fenster für 5 Multiple Passwörter
- [ ] "Alle kopieren" Funktion im Multiple-Fenster
- [ ] Historie-Fenster mit scrollbarer Liste
- [ ] Zeitstempel für jedes generierte Passwort
- [ ] Passwort-Stärke in der Historie
- [ ] "Historie löschen" Funktion mit Bestätigung
- [ ] Begrenzung auf letzte 20 Passwörter

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **Data Structures:**
  - `list()` - Lists
  - `dict()` - Dictionaries
  - `.append()` - Add to List
  - List Slicing `[-20:]`
- **Date/Time:**
  - `datetime` Module
  - `datetime.now()`
  - `.strftime()` Formatting
- **Advanced Widgets:**
  - `tk.Toplevel()` - Popup Windows
  - `tk.Text()` - Multi-line Text
  - `tk.Scrollbar()` - Scrolling
  - `.configure(yscrollcommand=)`
- **Text Widget Methods:**
  - `.insert()`
  - `.config(state=)`
  - `tk.END` Constant
- **MessageBox Advanced:**
  - `askyesno()` - Confirmation Dialog
- **Window Management:**
  - Parent-Child Relationships
  - `.destroy()` Method

### **Praktische Aufgaben:**
1. [ ] **`password_gen_step5.py` implementieren:**
   - Liste `self.password_history = []`
   - Funktion `add_to_history(password)`
   - Multiple Passwort-Generierung (5 Stück)
   - Toplevel-Fenster für Anzeigen
   - Historie-Fenster mit Scrollbar

2. [ ] **Popup-Fenster:**
   - `tk.Toplevel()` für neue Fenster
   - Text-Widget mit Scrollbar
   - Parent-Child Fenster-Beziehungen

<br/>

## 🚀 **Schritt 6: Professionelle Features & Finale Version**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Einstellungen automatisch speichern/laden (JSON-Datei)
- [ ] Export-Funktion für Historie (JSON/TXT)
- [ ] Datei-Dialog für Export-Pfad
- [ ] Professionelle Treeview-Tabelle für Historie
- [ ] "Mehrdeutige Zeichen ausschließen" Option
- [ ] Garantierter Zeichen-Mix Algorithmus
- [ ] Threading für bessere GUI-Performance
- [ ] Erweiterte Passwort-Stärke Bewertung (Score-System)
- [ ] Sauberes Beenden mit Einstellungen-Speicherung
- [ ] Vollständige Fehlerbehandlung für alle Funktionen

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **File I/O:**
  - `open()` Function
  - `with` Statement
  - `json.dump()`, `json.load()`
  - `os.path.exists()`
- **File Dialogs:**
  - `tkinter.filedialog`
  - `asksaveasfilename()`
  - `filetypes=` Parameter
- **Advanced Widgets:**
  - `tkinter.ttk` Module
  - `ttv.Treeview()` - Table Widget
  - `ttk.Scrollbar()`
- **Threading:**
  - `threading` Module
  - `threading.Thread()`
  - `daemon=True`
  - `.after()` Method for GUI Updates
- **Advanced Algorithms:**
  - `random.shuffle()`
  - `set()` for Unique Characters
  - List Comprehensions with Conditions
- **Window Events:**
  - `protocol()` Method
  - `WM_DELETE_WINDOW` Event
- **Error Handling:**
  - Multiple Exception Types
  - `try/except/finally`
  - Graceful Error Recovery

### **Praktische Aufgaben:**
1. [ ] **Finale Features implementieren:**
   - Einstellungen speichern/laden
   - Export-Funktionalität
   - Treeview für professionelle Tabellen  
   - Threading für bessere Performance
   - Mehrdeutige Zeichen ausschließen
   - Garantierter Zeichen-Mix Algorithmus

2. [ ] **Code-Qualität:**
   - Code-Kommentare überarbeiten
   - Funktionen dokumentieren
   - Error-Cases testen
   - Performance optimieren

---

## 📝 **Abschluss & Präsentation (optional)**

### **Aufgaben:**
- [ ] **Demo vorbereiten:**
  - 5-Minuten Präsentation der Anwendung
  - Vorher/Nachher Vergleich (Schritt 1 vs. Schritt 6)
  - Herausforderungen und Lösungen erklären

- [ ] **Code-Review:**
  - Wichtigste Lerninhalte zusammenfassen
  - Best Practices diskutieren
  - Verbesserungsvorschläge besprechen