# 📋 **Projekt Ablaufplan: MessengerService-Entwicklung**

## 📚 **Zusätzliche Ressourcen:**

- **Interaktive Python Lernplatform:** https://www.w3schools.com/python/
- **Python Dokumentation:** https://docs.python.org/3/
- **tkinter Tutorial:** https://guipy.de/doku.php?id=de:tkinter
- **socket Modul (Netzwerk):** https://docs.python.org/3/library/socket.html
- **threading in Python:** https://docs.python.org/3/library/threading.html
- **json Modul:** https://docs.python.org/3/library/json.html

**Viel Erfolg bei der Umsetzung! 🚀**

---

## 💡 **Grundidee des Projekts:**

Wir bauen einen lokalen Chat-Messenger mit einem **Server in der Mitte** und mehreren
**Clients** (GUI). Alles läuft **lokal auf deinem Rechner** über `127.0.0.1` (localhost) —
**kein Internet, kein externes Netzwerk**.

```
        ┌──────────────┐
        │    SERVER     │   <- vermittelt alle Nachrichten (Broadcast)
        │ 127.0.0.1:5.. │
        └──────┬───────┘
        ┌──────┴───────┐
   ┌────┴────┐    ┌────┴────┐
   │ Client A │    │ Client B │   <- GUI-Fenster, schreiben miteinander
   └─────────┘    └─────────┘
```

**Wichtig zum Starten:** Jeder Schritt ist EINE Datei, die in zwei Modi läuft. Öffne dazu
**mehrere Terminals**:

```
Terminal 1 (Server):  python messenger_stepN.py server
Terminal 2 (Client):  python messenger_stepN.py client
Terminal 3 (Client):  python messenger_stepN.py client
```

---

## 🎯 **Nach jedem Schritt:**

### **Checkpoint-Aufgaben:**
- [ ] Kurze Reflexion: Was lief gut? Was war schwierig?
- [ ] Server + zwei Clients gleichzeitig starten und testen
- [ ] Socket-Konzepte (bind, listen, accept, connect) verstehen
- [ ] Threading-Konzepte durchgehen (ein Thread pro Client)
- [ ] Nachrichten-Protokoll (JSON + Newline) nachvollziehen

### **Debugging-Tipps:**
- [ ] `print()` Statements im Server nutzen (Server zeigt alles in der Konsole)
- [ ] **Port belegt (WinError 10048):** immer `SO_REUSEADDR` setzen; sonst `PORT` oben ändern
- [ ] **tkinter ist nicht thread-safe:** GUI nur über `window.after(...)` oder `queue.Queue` aktualisieren
- [ ] **Umlaute/Emojis kaputt:** immer explizit mit `utf-8` kodieren/dekodieren
- [ ] **TCP-Framing:** nie annehmen „1 `recv` = 1 Nachricht" → Newline-JSON-Puffer nutzen
- [ ] **Server lässt sich nicht mit Strg+C beenden:** Ein blockierendes `accept()`/`recv()` lässt das Signal unter Windows nicht durch. Lösung: `server_socket.settimeout(1.0)` setzen und `except socket.timeout: continue` in der Schleife — so bricht der Aufruf jede Sekunde kurz ab und Strg+C greift
- [ ] **Firewall:** Bindung an `127.0.0.1` (nicht `0.0.0.0`) → keine Windows-Firewall-Abfrage
- [ ] **Doppelklick startet nichts:** immer aus einem Terminal mit `server`/`client` starten

---

## 🚀 **Schritt 1: Socket-Grundlagen — Echo-Server & CLI-Client**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] TCP-Socket erstellen (`socket.socket`)
- [ ] Server: `bind`, `listen`, `accept` (eine Verbindung)
- [ ] Client: `connect` zum Server auf `127.0.0.1`
- [ ] Eine Nachricht senden (`sendall`) und empfangen (`recv`)
- [ ] Echo: Server schickt die Nachricht in Großbuchstaben zurück
- [ ] `SO_REUSEADDR` setzen, damit der Port sofort wieder frei ist
- [ ] Sauberes Beenden mit `quit`, `try/except`, `KeyboardInterrupt`
- [ ] Modus-Auswahl über `sys.argv` (`server` / `client`)

### **💡 Kurz erklärt (ohne Code):**
- **Socket = Steckdose fürs Netzwerk:** Server und Client verbinden sich über eine Adresse + Port.
  - Beispiel: Der Server „wohnt" unter `127.0.0.1:50007`, der Client klingelt dort an.
- **Server-Ablauf:** Der Server bindet sich an den Port, lauscht und wartet auf eine Verbindung.
  - Beispiel: `accept()` blockiert so lange, bis sich der erste Client meldet.
- **Echo-Prinzip:** Was der Server empfängt, schickt er zurück (hier in GROSSBUCHSTABEN).
  - Beispiel: „hallo" → der Client bekommt „HALLO" zurück.
- **Port wieder freigeben:** Ohne `SO_REUSEADDR` bleibt der Port kurz „belegt".
  - Beispiel: Startest du den Server sofort neu, gäbe es sonst „Port belegt".

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **socket Modul:**
  - `socket.socket(AF_INET, SOCK_STREAM)` — TCP-Socket
  - `.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)`
  - `.bind()`, `.listen()`, `.accept()`
  - `.connect()`, `.recv()`, `.sendall()`, `.close()`
- **String Operations:**
  - `.encode("utf-8")` / `.decode("utf-8")`
  - `.upper()`, `.strip()`
- **Control Flow & Error Handling:**
  - `while` Loop, `if/else`, `break`
  - `try/except` (`OSError`, `ConnectionRefusedError`, `KeyboardInterrupt`)
- **Programm-Argumente:**
  - `sys.argv`

### **Praktische Aufgaben:**
1. [ ] **`messenger_step1.py` implementieren:**
   - `MessengerServer` mit `start()` (bind/listen/accept/echo)
   - `MessengerClient` mit `start()` (connect/send/recv)
   - Modus über `sys.argv` auswählen
2. [ ] **Testen (2 Terminals):**
   - `python messenger_step1.py server`
   - `python messenger_step1.py client` → Nachricht tippen → Echo prüfen

<br/>

## 🔧 **Schritt 2: Multi-Client CLI-Chat — Threading & Broadcast**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Server nimmt mehrere Clients an (Endlosschleife um `accept`)
- [ ] Ein Thread pro Client (`threading.Thread`, `daemon=True`)
- [ ] Gemeinsame Client-Liste mit `threading.Lock` schützen
- [ ] Broadcast: Nachricht von A geht an alle anderen Clients
- [ ] Nachrichten-Protokoll: newline-getrenntes JSON
- [ ] Empfangs-Puffer, der bei `"\n"` aufteilt (Stream-Framing)
- [ ] Client mit Hintergrund-Empfangs-Thread + Eingabe-Schleife
- [ ] Sauberes Entfernen bei Verbindungsabbruch (`recv` == leer)

### **💡 Kurz erklärt (ohne Code):**
- **Ein Thread pro Client:** Damit mehrere Nutzer gleichzeitig bedient werden.
  - Beispiel: Während Alice tippt, kann Bob unabhängig schreiben.
- **Broadcast:** Der Server verteilt eine Nachricht an alle außer dem Absender.
  - Beispiel: Alice schreibt „Hi" → Bob (und alle anderen) sehen es.
- **JSON + Newline-Framing:** TCP ist ein Byte-Strom ohne Grenzen, deshalb trennen wir Nachrichten mit `"\n"`.
  - Beispiel: Zwei schnelle Nachrichten kommen sonst als ein Klumpen an — das `"\n"` trennt sie sauber.
- **Lock für gemeinsame Daten:** Mehrere Threads greifen auf dieselbe Client-Liste zu.
  - Beispiel: Das Lock verhindert, dass zwei Threads die Liste gleichzeitig verändern.

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **threading:**
  - `threading.Thread(target=..., args=..., daemon=True)`
  - `threading.Lock()` mit `with lock:`
- **json:**
  - `json.dumps()` / `json.loads()`
- **Framing-Logik:**
  - String-Puffer + `.split("\n", 1)`
  - `while "\n" in buffer`
- **Datenstrukturen:**
  - `list` (Clients), Kopie mit `list(...)` beim Iterieren

### **Praktische Aufgaben:**
1. [ ] **`messenger_step2.py` implementieren:**
   - `send_message()` / `receive_messages()` (Framing-Helfer)
   - `handle_client()` in eigenem Thread
   - `broadcast(msg, exclude=sender)`
2. [ ] **Testen (3 Terminals):**
   - 1 Server + 2 Clients starten
   - In Client A tippen → erscheint in Client B (und umgekehrt)

<br/>

## 🖥️ **Schritt 3: Erste GUI mit Benutzernamen & Design**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] `client`-Modus öffnet ein tkinter-Fenster
- [ ] Chat-Anzeige (`scrolledtext.ScrolledText`), Eingabefeld (`tk.Entry`), „Senden"-Button
- [ ] Enter-Taste sendet (`bind("<Return>")`), Fokus im Eingabefeld
- [ ] Verbindungsaufbau beim Start + Hintergrund-Empfangs-Thread
- [ ] Thread-sichere Anzeige über `window.after(0, ...)`
- [ ] Benutzername beim Start abfragen (`simpledialog.askstring`) + `join`-Nachricht
- [ ] Nachrichten mit Benutzername + Zeitstempel
- [ ] Farbiger Header (`#2196F3`) + Farb-Tags (eigene vs. fremde Nachrichten)
- [ ] Beitritts-/Verlassen-Hinweise (`system`-Nachrichten)
- [ ] Server bleibt headless (Konsole) wie in Schritt 2, merkt sich `{Socket: Benutzername}`

### **💡 Kurz erklärt (ohne Code):**
- **GUI statt Terminal:** Der Client bekommt ein richtiges Chat-Fenster.
  - Beispiel: Statt in die Konsole zu tippen, nutzt man ein Eingabefeld mit „Senden".
- **Empfangs-Thread im Hintergrund:** Die GUI bleibt bedienbar, während Nachrichten ankommen.
  - Beispiel: Man kann tippen, auch wenn gerade eine Nachricht eintrifft.
- **tkinter ist nicht thread-safe:** Der Empfangs-Thread darf Widgets nie direkt anfassen.
  - Beispiel: Er reicht neue Nachrichten mit `window.after(0, ...)` sicher an das Fenster weiter.
- **Benutzernamen + Zeitstempel:** Jeder hat einen Namen, jede Nachricht eine Uhrzeit.
  - Beispiel: `[14:35] Alice: Hallo` statt nur „Andere: Hallo".
- **Beitritts-/Verlassen-Hinweise:** Der Server meldet, wer kommt und geht.
  - Beispiel: „🟢 Bob ist beigetreten" / „🔴 Bob hat den Chat verlassen".
- **Farb-Tags:** Eigene Nachrichten blau, fremde grün, System-Hinweise grau.
  - Beispiel: Man erkennt sofort, was von einem selbst kommt.

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **tkinter Basics:**
  - `tk.Tk()`, `tk.Frame()`, `tk.Label()`, `tk.Entry()`, `tk.Button()`
  - `.pack()` mit `fill`, `expand`, `padx`, `pady`, `pack_propagate(False)`
- **Erweiterte Widgets:**
  - `tkinter.scrolledtext.ScrolledText`
  - `tkinter.simpledialog.askstring`
- **Text Widget + Farb-Tags:**
  - `.insert(tk.END, text, tag)`, `.see(tk.END)`, `state=tk.DISABLED`
  - `.tag_config(name, foreground=...)`
- **Events:**
  - `command=`, `.bind("<Return>", ...)`, `.focus()`
- **Thread-sichere GUI:**
  - `window.after(0, funktion, argument)`
- **Date/Time:**
  - `datetime.now().strftime("[%H:%M]")`

### **Praktische Aufgaben:**
1. [ ] **`messenger_step3.py` implementieren:**
   - Namensabfrage vor dem Hauptfenster (`simpledialog`)
   - `MessengerClientGUI` mit `setup_gui()` (ScrolledText, Eingabe, Header, Farb-Tags)
   - `receive_loop()` im Thread + `window.after(0, self.handle_incoming, ...)`
   - `join`-Protokoll + `system`-Hinweise im Server
2. [ ] **Testen (3 Terminals):**
   - Server + zwei Client-Fenster („Alice"/„Bob") → Namen, Zeitstempel, Join/Leave prüfen

<br/>

## 📊 **Schritt 4: Threading-Robustheit & UX**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] `queue.Queue` + `window.after(100, poll_queue)` für sichere GUI-Updates
- [ ] Verbindungsstatus-Anzeige (🟢 Verbunden / 🔴 Getrennt)
- [ ] Online-Benutzerliste (`tk.Listbox`), Server sendet `userlist`
- [ ] „Neu verbinden"-Button bei Verbindungsverlust
- [ ] Sauberes Beenden (`protocol("WM_DELETE_WINDOW", on_close)`)
- [ ] Robuste Fehlerbehandlung (`ConnectionResetError`, `OSError`)

### **💡 Kurz erklärt (ohne Code):**
- **Queue statt vieler after(0):** Der Empfangs-Thread legt Nachrichten in eine Warteschlange, die GUI leert sie regelmäßig.
  - Beispiel: Alle 100 ms schaut die GUI nach, ob neue Nachrichten da sind.
- **Statusanzeige:** Man sieht sofort, ob die Verbindung steht.
  - Beispiel: Stoppt der Server, wird die Anzeige rot („🔴 Getrennt").
- **Userliste:** Rechts sieht man, wer gerade online ist.
  - Beispiel: Tritt Bob bei, erscheint „• Bob" in der Liste bei allen.
- **Sauberes Beenden:** Beim Schließen wird der Server informiert, keine Fehlermeldung.
  - Beispiel: Schließt Alice ihr Fenster, sehen die anderen „🔴 Alice hat den Chat verlassen".

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **queue:**
  - `queue.Queue()`, `.put()`, `.get_nowait()`, `queue.Empty`
- **Periodische GUI-Updates:**
  - `window.after(100, self.poll_queue)`
- **Weitere Widgets:**
  - `tk.Listbox` mit `.insert()`, `.delete(0, tk.END)`
- **Fenster-Events:**
  - `window.protocol("WM_DELETE_WINDOW", on_close)`
- **Fehlerbehandlung:**
  - `ConnectionResetError`, `OSError`

### **Praktische Aufgaben:**
1. [ ] **`messenger_step4.py` implementieren:**
   - `poll_queue()` + `incoming`-Queue
   - `broadcast_userlist()` im Server
   - Status-Label, Reconnect-Button, `on_close()`
2. [ ] **Testen:** Userliste live prüfen, Server stoppen → Status rot → Neu verbinden

<br/>

## 🚀 **Schritt 5: Professionelle Features & Finale Version**

### **📋 Features Checkliste für diesen Schritt:**
- [ ] Persistenz: Server speichert Verlauf in `chat_log.json` (JSON-Zeile pro Nachricht)
- [ ] Verlauf-Replay: neue Clients erhalten die letzten N Nachrichten (`history`)
- [ ] Private Nachrichten mit `/w <Name> <Text>` (`private`)
- [ ] Tipp-Anzeige („X schreibt ...") über `typing`, gedrosselt
- [ ] Buttons: Senden, Löschen, Export (Chat als Textdatei)
- [ ] Zentrale Konfiguration (`HOST`, `PORT`, `LOG_DATEI`, `HISTORY_SIZE`)

### **💡 Kurz erklärt (ohne Code):**
- **Persistenz:** Der Server merkt sich den Verlauf auch nach einem Neustart.
  - Beispiel: `chat_log.json` sammelt alle Nachrichten Zeile für Zeile.
- **Verlauf-Replay:** Wer später beitritt, sieht die letzten Nachrichten.
  - Beispiel: Bob kommt dazu und liest die letzten 20 Nachrichten nach.
- **Private Nachrichten:** Nur ein bestimmter Nutzer bekommt die Nachricht.
  - Beispiel: `/w Bob geheim` erreicht nur Bob (und dich selbst).
- **Tipp-Anzeige:** Man sieht, wenn jemand gerade schreibt.
  - Beispiel: Unten steht kurz „✍️ Alice schreibt ...".

### **🔧 Benötigte Python-Funktionen/Strukturen:**
- **File I/O:**
  - `open(..., "a", encoding="utf-8")` (anhängen)
  - `os.path.exists()`
  - JSON-Zeilen lesen/schreiben
- **Weitere GUI-Elemente:**
  - `filedialog.asksaveasfilename()`
  - `messagebox.showinfo/showerror`
- **Routing-Logik:**
  - Ziel-Socket über Namen suchen (`dict`-Suche unter Lock)
- **Drosselung:**
  - `window.after(2000, reset)` für Tipp-Hinweis

### **Praktische Aufgaben:**
1. [ ] **`messenger_step5_final.py` implementieren:**
   - `save_to_log()` / `load_history()` + `history`-Replay
   - `route_private()` + `/w`-Parsing im Client
   - `typing`-Hinweis, Export/Löschen-Buttons
2. [ ] **Finale Version testen:**
   - Nachzügler sieht Verlauf
   - `/w Name Text` erreicht nur den Ziel-Client
   - `chat_log.json` prüfen

---

## 📝 **Abschluss & Präsentation (optional)**

### **Aufgaben:**
- [ ] **Demo vorbereiten:**
  - 5-Minuten-Präsentation (Server + zwei Clients live)
  - Vorher/Nachher-Vergleich (Schritt 1 CLI vs. Schritt 5 GUI)
  - Socket-Ablauf (bind/listen/accept/connect) erklären
  - Threading- und Broadcast-Prinzip zeigen

- [ ] **Code-Review:**
  - Wichtigste Lerninhalte zusammenfassen
  - CLI- vs. GUI-Entwicklung vergleichen
  - Warum newline-JSON-Framing? (TCP-Stream)
  - tkinter-Thread-Sicherheit (`after`/`queue`) besprechen

- [ ] **Erweiterungsideen diskutieren:**
  - Mehr als 2 Clients / Chaträume (Rooms)
  - Verschlüsselung der Nachrichten
  - Datei-Übertragung zwischen Clients
  - Umstieg von localhost auf echtes Netzwerk (mehrere Rechner)
