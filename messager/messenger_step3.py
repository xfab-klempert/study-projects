"""
Schritt 3: Erste GUI (tkinter) mit Benutzernamen & Design

Ziel: Der CLI-Client aus Schritt 2 wird durch ein grafisches Chat-Fenster ersetzt.
Gleich richtig schoen: mit Benutzernamen, Zeitstempeln und Farben.
Der Server bleibt headless (Konsole) wie in Schritt 2.

Neu in diesem Schritt (erste GUI!):
- tkinter GUI: Chat-Anzeige, Eingabefeld, Senden-Button
- Empfangs-Thread im Hintergrund + window.after(0, ...) fuer thread-sichere Updates
  (WICHTIG: tkinter ist nicht thread-safe -> nie Widgets direkt aus dem Thread anfassen)
- simpledialog.askstring: fragt beim Start den Benutzernamen ab
- scrolledtext.ScrolledText: Chat-Bereich mit automatischer Scroll-Leiste
- datetime: Zeitstempel wie [14:35]
- Farbiger Header + Farb-Tags (eigene vs. fremde Nachrichten)
- Server merkt sich {Socket: Benutzername} und sendet system-Hinweise

So startest du diesen Schritt (drei Terminals):
    Terminal 1 (Server):  python messenger_step3.py server
    Terminal 2 (Client):  python messenger_step3.py client   -> Name "Alice"
    Terminal 3 (Client):  python messenger_step3.py client   -> Name "Bob"
"""

import socket
import sys
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime

HOST = "127.0.0.1"
PORT = 50007
ENCODING = "utf-8"

# Windows-Konsole auf UTF-8 umstellen, damit Emojis/Umlaute nicht abstuerzen
try:
    sys.stdout.reconfigure(encoding=ENCODING)
except Exception:
    pass


# --- Framing-Helfer --------------------------------------------------------
def send_message(sock, message_dict):
    daten = (json.dumps(message_dict) + "\n").encode(ENCODING)
    sock.sendall(daten)


def receive_messages(sock, buffer):
    daten = sock.recv(4096)
    if not daten:
        return None, buffer
    buffer += daten.decode(ENCODING)
    nachrichten = []
    while "\n" in buffer:
        zeile, buffer = buffer.split("\n", 1)
        if zeile.strip():
            nachrichten.append(json.loads(zeile))
    return nachrichten, buffer


def zeitstempel():
    """Gibt die aktuelle Uhrzeit als [HH:MM] zurueck."""
    return datetime.now().strftime("[%H:%M]")


# --- Server ----------------------------------------------------------------
class MessengerServer:
    def __init__(self):
        self.server_socket = None
        self.clients = {}                 # {conn: username}
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            # Timeout: accept() bricht jede Sekunde kurz ab, damit Strg+C funktioniert
            self.server_socket.settimeout(1.0)
            print(f"🟢 Chat-Server laeuft auf {HOST}:{PORT}")
            print("⏳ Warte auf Clients... (Strg+C zum Beenden)")
            while True:
                try:
                    conn, addr = self.server_socket.accept()
                except socket.timeout:
                    continue  # kein Client -> weiter warten (Strg+C wurde geprueft)
                threading.Thread(
                    target=self.handle_client, args=(conn, addr), daemon=True
                ).start()
        except OSError as e:
            print(f"❌ Server-Fehler: {e}")
            print(f"💡 Tipp: Ist Port {PORT} belegt? Aendere PORT oder warte kurz.")
        except KeyboardInterrupt:
            print("\n👋 Server wird beendet.")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, conn, addr):
        buffer = ""
        username = None
        try:
            while True:
                nachrichten, buffer = receive_messages(conn, buffer)
                if nachrichten is None:
                    break
                for msg in nachrichten:
                    typ = msg.get("type")

                    if typ == "join":
                        username = msg.get("username", "Unbekannt")
                        with self.lock:
                            self.clients[conn] = username
                        print(f"✅ {username} ist beigetreten ({addr})")
                        self.broadcast(
                            {"type": "system", "text": f"🟢 {username} ist beigetreten"},
                            exclude=conn,
                        )

                    elif typ == "chat":
                        # Server ergaenzt Name + Zeitstempel (autoritativ)
                        weiter = {
                            "type": "chat",
                            "username": username or "Unbekannt",
                            "text": msg.get("text", ""),
                            "time": zeitstempel(),
                        }
                        print(f"📩 {weiter['time']} {weiter['username']}: {weiter['text']}")
                        self.broadcast(weiter, exclude=conn)

        except (ConnectionResetError, OSError):
            pass
        finally:
            self.remove_client(conn, username)

    def broadcast(self, message_dict, exclude=None):
        with self.lock:
            for client in list(self.clients):
                if client is exclude:
                    continue
                try:
                    send_message(client, message_dict)
                except OSError:
                    pass

    def remove_client(self, conn, username):
        with self.lock:
            if conn in self.clients:
                del self.clients[conn]
        conn.close()
        if username:
            print(f"🔴 {username} hat den Chat verlassen")
            self.broadcast(
                {"type": "system", "text": f"🔴 {username} hat den Chat verlassen"}
            )


# --- GUI-Client ------------------------------------------------------------
class MessengerClientGUI:
    def __init__(self, username):
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

        self.window = tk.Tk()
        self.window.title(f"📨 MessengerService - {username}")
        self.window.geometry("520x560")
        self.window.configure(bg="#f0f0f0")

        self.setup_gui()
        self.connect()

    def setup_gui(self):
        # Farbiger Header
        header = tk.Frame(self.window, bg="#2196F3", height=55)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text=f"📨 MessengerService  -  {self.username}",
            font=("Arial", 15, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(pady=12)

        # Chat-Bereich mit Scrollbar
        self.chat_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#333333",
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Farb-Tags fuer verschiedene Nachrichtentypen
        self.chat_area.tag_config("own", foreground="#1976D2")     # eigene: blau
        self.chat_area.tag_config("other", foreground="#388E3C")   # fremde: gruen
        self.chat_area.tag_config("system", foreground="#9E9E9E", font=("Arial", 9, "italic"))

        # Eingabe-Bereich
        input_frame = tk.Frame(self.window, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.input_field = tk.Entry(
            input_frame, font=("Arial", 12), relief=tk.RAISED, bd=2, bg="#ffffff"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message_action)
        self.input_field.focus()

        tk.Button(
            input_frame,
            text="Senden",
            command=self.send_message_action,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=20,
        ).pack(side=tk.RIGHT)

    def connect(self):
        try:
            self.client_socket.connect((HOST, PORT))
            # Beitritt mit Namen anmelden
            send_message(self.client_socket, {"type": "join", "username": self.username})
            self.display_message("✅ Mit Server verbunden. Los geht's!", "system")
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except ConnectionRefusedError:
            self.display_message("❌ Server nicht erreichbar. Laeuft er schon?", "system")

    def display_message(self, text, tag=None):
        """Schreibt eine Zeile mit optionaler Farbe (nur im Haupt-Thread!)."""
        self.chat_area.config(state=tk.NORMAL)
        if tag:
            self.chat_area.insert(tk.END, text + "\n", tag)
        else:
            self.chat_area.insert(tk.END, text + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def send_message_action(self, event=None):
        text = self.input_field.get().strip()
        if not text:
            return
        try:
            send_message(self.client_socket, {"type": "chat", "text": text})
            self.display_message(f"{zeitstempel()} Du: {text}", "own")
            self.input_field.delete(0, tk.END)
        except OSError:
            self.display_message("❌ Senden fehlgeschlagen (keine Verbindung).", "system")

    def receive_loop(self):
        buffer = ""
        try:
            while self.running:
                nachrichten, buffer = receive_messages(self.client_socket, buffer)
                if nachrichten is None:
                    self.window.after(0, self.display_message,
                                      "🔴 Verbindung zum Server verloren.", "system")
                    break
                for msg in nachrichten:
                    self.window.after(0, self.handle_incoming, msg)
        except (ConnectionResetError, OSError):
            pass

    def handle_incoming(self, msg):
        """Zeigt eine empfangene Nachricht je nach Typ an (Haupt-Thread)."""
        typ = msg.get("type")
        if typ == "chat":
            zeile = f"{msg.get('time', '')} {msg.get('username', '?')}: {msg.get('text', '')}"
            self.display_message(zeile, "other")
        elif typ == "system":
            self.display_message(msg.get("text", ""), "system")

    def run(self):
        self.window.mainloop()
        self.running = False
        self.client_socket.close()


def print_usage():
    print("=" * 55)
    print("  📨 MessengerService - Schritt 3 (Erste GUI: Namen & Design)")
    print("=" * 55)
    print("Starte in mehreren TERMINALS:")
    print()
    print("  Terminal 1 (Server):  python messenger_step3.py server")
    print("  Terminal 2 (Client):  python messenger_step3.py client")
    print("  Terminal 3 (Client):  python messenger_step3.py client")
    print()
    print("=" * 55)


if __name__ == "__main__":
    modus = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if modus == "server":
        MessengerServer().start()
    elif modus == "client":
        try:
            # Namen abfragen (kleines Dialogfenster vor dem Chat)
            temp = tk.Tk()
            temp.withdraw()  # Hauptfenster verstecken, nur Dialog zeigen
            name = simpledialog.askstring("Benutzername", "Wie heisst du?", parent=temp)
            temp.destroy()
            if not name:
                name = "Gast"
            MessengerClientGUI(name).run()
        except Exception as e:
            print(f"Fehler beim Starten: {e}")
            input("Druecke Enter zum Beenden...")
    else:
        print_usage()
        input("Druecke Enter zum Beenden...")
