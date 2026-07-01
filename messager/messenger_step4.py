"""
Schritt 4: Threading-Robustheit + UX (Status, Userliste, sauberes Beenden)

Ziel: Der Messenger wird stabil und komfortabel. Er zeigt den Verbindungsstatus,
eine Liste der Online-Nutzer, kann sich neu verbinden und beendet sich sauber.

Neu in diesem Schritt:
- queue.Queue + window.after(100, poll_queue): robuster Weg, Nachrichten aus dem
  Empfangs-Thread sicher in die GUI zu bringen (statt vieler einzelner .after(0,...))
- Status-Label (🟢 Verbunden / 🔴 Getrennt)
- Online-Userliste (tk.Listbox), Server sendet userlist bei Join/Leave
- "Neu verbinden"-Button und sauberes Schliessen (WM_DELETE_WINDOW)

So startest du diesen Schritt (drei Terminals):
    Terminal 1 (Server):  python messenger_step4.py server
    Terminal 2 (Client):  python messenger_step4.py client
    Terminal 3 (Client):  python messenger_step4.py client
"""

import socket
import sys
import json
import threading
import queue
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
                        self.broadcast_userlist()
                    elif typ == "chat":
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

    def broadcast_userlist(self):
        """Schickt die aktuelle Liste aller Online-Nutzer an alle Clients."""
        with self.lock:
            users = list(self.clients.values())
        self.broadcast({"type": "userlist", "users": users})

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
            self.broadcast_userlist()


# --- GUI-Client ------------------------------------------------------------
class MessengerClientGUI:
    def __init__(self, username):
        self.username = username
        self.client_socket = None
        self.running = False
        self.incoming = queue.Queue()     # Thread -> GUI Uebergabe

        self.window = tk.Tk()
        self.window.title(f"📨 MessengerService - {username}")
        self.window.geometry("640x580")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_gui()
        self.connect()

        # Regelmaessig die Queue leeren (thread-sicher, im Haupt-Thread)
        self.window.after(100, self.poll_queue)

    def setup_gui(self):
        # Header mit Status-Anzeige
        header = tk.Frame(self.window, bg="#2196F3", height=55)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text=f"📨 {self.username}", font=("Arial", 15, "bold"),
            bg="#2196F3", fg="white",
        ).pack(side=tk.LEFT, padx=15, pady=12)
        self.status_label = tk.Label(
            header, text="🔴 Getrennt", font=("Arial", 11, "bold"),
            bg="#2196F3", fg="white",
        )
        self.status_label.pack(side=tk.RIGHT, padx=15)

        # Mittlerer Bereich: Chat links, Userliste rechts
        mitte = tk.Frame(self.window, bg="#f0f0f0")
        mitte.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.chat_area = scrolledtext.ScrolledText(
            mitte, wrap=tk.WORD, font=("Arial", 10), bg="#ffffff", fg="#333333",
            relief=tk.RAISED, bd=2, state=tk.DISABLED,
        )
        self.chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_area.tag_config("own", foreground="#1976D2")
        self.chat_area.tag_config("other", foreground="#388E3C")
        self.chat_area.tag_config("system", foreground="#9E9E9E", font=("Arial", 9, "italic"))

        # Userliste rechts
        user_frame = tk.Frame(mitte, bg="#f0f0f0")
        user_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        tk.Label(user_frame, text="👥 Online", font=("Arial", 10, "bold"),
                 bg="#f0f0f0", fg="#333333").pack()
        self.user_listbox = tk.Listbox(user_frame, width=16, font=("Arial", 10),
                                       relief=tk.RAISED, bd=2)
        self.user_listbox.pack(fill=tk.Y, expand=True)

        # Eingabe-Bereich
        input_frame = tk.Frame(self.window, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.input_field = tk.Entry(input_frame, font=("Arial", 12), relief=tk.RAISED,
                                    bd=2, bg="#ffffff")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message_action)
        self.input_field.focus()
        tk.Button(input_frame, text="Senden", command=self.send_message_action,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  relief=tk.RAISED, bd=2, padx=20).pack(side=tk.RIGHT)

        # Button-Zeile: Neu verbinden
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.reconnect_button = tk.Button(
            button_frame, text="🔄 Neu verbinden", command=self.connect,
            bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
            relief=tk.RAISED, bd=2, padx=15,
        )
        self.reconnect_button.pack(side=tk.LEFT)

    def set_status(self, verbunden):
        """Aktualisiert das Status-Label (gruen/rot)."""
        if verbunden:
            self.status_label.config(text="🟢 Verbunden")
        else:
            self.status_label.config(text="🔴 Getrennt")

    def connect(self):
        """Baut (oder erneuert) die Verbindung zum Server auf."""
        if self.running:
            return  # schon verbunden
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
            self.running = True
            self.set_status(True)
            send_message(self.client_socket, {"type": "join", "username": self.username})
            self.display_message("✅ Mit Server verbunden.", "system")
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except ConnectionRefusedError:
            self.set_status(False)
            self.display_message("❌ Server nicht erreichbar. Spaeter neu verbinden.", "system")

    def display_message(self, text, tag=None):
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
        if not self.running:
            self.display_message("❌ Nicht verbunden. Klicke 'Neu verbinden'.", "system")
            return
        try:
            send_message(self.client_socket, {"type": "chat", "text": text})
            self.display_message(f"{zeitstempel()} Du: {text}", "own")
            self.input_field.delete(0, tk.END)
        except OSError:
            self.set_status(False)
            self.running = False
            self.display_message("❌ Senden fehlgeschlagen (Verbindung weg).", "system")

    def receive_loop(self):
        """Hintergrund-Thread: legt Nachrichten nur in die Queue (nie GUI anfassen!)."""
        buffer = ""
        try:
            while self.running:
                nachrichten, buffer = receive_messages(self.client_socket, buffer)
                if nachrichten is None:
                    self.incoming.put({"type": "_disconnect"})
                    break
                for msg in nachrichten:
                    self.incoming.put(msg)
        except (ConnectionResetError, OSError):
            self.incoming.put({"type": "_disconnect"})

    def poll_queue(self):
        """Laeuft alle 100 ms im Haupt-Thread und verarbeitet neue Nachrichten."""
        try:
            while True:
                msg = self.incoming.get_nowait()
                self.handle_incoming(msg)
        except queue.Empty:
            pass
        # sich selbst wieder einplanen
        self.window.after(100, self.poll_queue)

    def handle_incoming(self, msg):
        typ = msg.get("type")
        if typ == "chat":
            zeile = f"{msg.get('time', '')} {msg.get('username', '?')}: {msg.get('text', '')}"
            self.display_message(zeile, "other")
        elif typ == "system":
            self.display_message(msg.get("text", ""), "system")
        elif typ == "userlist":
            self.update_userlist(msg.get("users", []))
        elif typ == "_disconnect":
            self.running = False
            self.set_status(False)
            self.user_listbox.delete(0, tk.END)
            self.display_message("🔴 Verbindung zum Server verloren.", "system")

    def update_userlist(self, users):
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, f"• {user}")

    def on_close(self):
        """Sauberes Beenden: Socket schliessen, dann Fenster zerstoeren."""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except OSError:
                pass
        self.window.destroy()

    def run(self):
        self.window.mainloop()


def print_usage():
    print("=" * 55)
    print("  📨 MessengerService - Schritt 4 (Robustheit + UX)")
    print("=" * 55)
    print("Starte in mehreren TERMINALS:")
    print()
    print("  Terminal 1 (Server):  python messenger_step4.py server")
    print("  Terminal 2 (Client):  python messenger_step4.py client")
    print("  Terminal 3 (Client):  python messenger_step4.py client")
    print()
    print("=" * 55)


if __name__ == "__main__":
    modus = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if modus == "server":
        MessengerServer().start()
    elif modus == "client":
        try:
            temp = tk.Tk()
            temp.withdraw()
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
