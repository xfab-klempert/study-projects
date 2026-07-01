"""
Schritt 5 (Finale Version): Professioneller MessengerService

Ziel: Der Messenger bekommt professionelle Funktionen und eine polierte Oberflaeche.

Neu in diesem Schritt:
- Persistenz: Der Server speichert den Chatverlauf in chat_log.json (eine JSON-Zeile
  pro Nachricht). Neue Clients bekommen die letzten Nachrichten (history-Replay).
- Private Nachrichten: "/w <Name> <Text>" schickt eine Fluester-Nachricht nur an einen
  bestimmten Nutzer (und an dich selbst).
- Tipp-Anzeige: "X schreibt ..." erscheint, waehrend jemand tippt.
- Buttons: Senden, Loeschen, Export (Chat als Textdatei speichern).
- Zentrale Konfiguration ganz oben.

So startest du diesen Schritt (drei Terminals):
    Terminal 1 (Server):  python messenger_step5_final.py server
    Terminal 2 (Client):  python messenger_step5_final.py client
    Terminal 3 (Client):  python messenger_step5_final.py client
"""

import socket
import sys
import os
import json
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, messagebox
from datetime import datetime

# ---------------------------------------------------------------------------
# Zentrale Konfiguration
# ---------------------------------------------------------------------------
HOST = "127.0.0.1"          # localhost -> kein Internet
PORT = 50007                # bei "Port belegt" hier aendern
ENCODING = "utf-8"          # fuer Umlaute und Emojis
LOG_DATEI = "chat_log.json" # hier speichert der Server den Verlauf
HISTORY_SIZE = 20           # so viele alte Nachrichten bekommt ein neuer Client

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
        self.history = self.load_history()

    def load_history(self):
        """Laedt die letzten Nachrichten aus der Log-Datei (falls vorhanden)."""
        if not os.path.exists(LOG_DATEI):
            return []
        verlauf = []
        try:
            with open(LOG_DATEI, "r", encoding=ENCODING) as f:
                for zeile in f:
                    zeile = zeile.strip()
                    if zeile:
                        verlauf.append(json.loads(zeile))
        except (OSError, json.JSONDecodeError):
            return []
        return verlauf[-HISTORY_SIZE:]

    def save_to_log(self, message_dict):
        """Haengt eine Nachricht als JSON-Zeile an die Log-Datei an."""
        try:
            with open(LOG_DATEI, "a", encoding=ENCODING) as f:
                f.write(json.dumps(message_dict) + "\n")
        except OSError:
            pass
        self.history.append(message_dict)
        self.history = self.history[-HISTORY_SIZE:]

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            # Timeout: accept() bricht jede Sekunde kurz ab, damit Strg+C funktioniert
            self.server_socket.settimeout(1.0)
            print(f"🟢 Chat-Server laeuft auf {HOST}:{PORT}")
            print(f"💾 Verlauf-Datei: {LOG_DATEI} ({len(self.history)} Nachrichten geladen)")
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
                        # Verlauf an den neuen Client schicken
                        try:
                            send_message(conn, {"type": "history", "messages": self.history})
                        except OSError:
                            pass
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
                        self.save_to_log(weiter)
                        self.broadcast(weiter, exclude=conn)

                    elif typ == "private":
                        self.route_private(conn, username, msg)

                    elif typ == "typing":
                        # Tipp-Hinweis an alle anderen weiterreichen
                        self.broadcast(
                            {"type": "typing", "username": username or "Jemand"},
                            exclude=conn,
                        )

        except (ConnectionResetError, OSError):
            pass
        finally:
            self.remove_client(conn, username)

    def route_private(self, sender_conn, sender_name, msg):
        """Schickt eine private Nachricht nur an den Ziel-Nutzer (und den Absender)."""
        ziel_name = msg.get("to", "")
        text = msg.get("text", "")
        privat = {
            "type": "private",
            "from": sender_name or "Unbekannt",
            "to": ziel_name,
            "text": text,
            "time": zeitstempel(),
        }
        # Ziel-Socket anhand des Namens suchen
        with self.lock:
            ziele = [c for c, name in self.clients.items() if name == ziel_name]
        if not ziele:
            # Ziel nicht gefunden -> Absender informieren
            try:
                send_message(sender_conn, {
                    "type": "system",
                    "text": f"❌ Nutzer '{ziel_name}' ist nicht online.",
                })
            except OSError:
                pass
            return
        for ziel in ziele:
            try:
                send_message(ziel, privat)
            except OSError:
                pass
        print(f"🔒 privat {sender_name} -> {ziel_name}: {text}")

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
        self.incoming = queue.Queue()
        self.typing_gesendet = False      # Drossel fuer die Tipp-Anzeige

        self.window = tk.Tk()
        self.window.title(f"📨 MessengerService - {username}")
        self.window.geometry("680x620")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_gui()
        self.connect()
        self.window.after(100, self.poll_queue)

    def setup_gui(self):
        # Header + Status
        header = tk.Frame(self.window, bg="#2196F3", height=55)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text=f"📨 {self.username}", font=("Arial", 15, "bold"),
                 bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=15, pady=12)
        self.status_label = tk.Label(header, text="🔴 Getrennt", font=("Arial", 11, "bold"),
                                     bg="#2196F3", fg="white")
        self.status_label.pack(side=tk.RIGHT, padx=15)

        # Mitte: Chat + Userliste
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
        self.chat_area.tag_config("private", foreground="#9C27B0", font=("Arial", 10, "bold"))

        user_frame = tk.Frame(mitte, bg="#f0f0f0")
        user_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        tk.Label(user_frame, text="👥 Online", font=("Arial", 10, "bold"),
                 bg="#f0f0f0", fg="#333333").pack()
        self.user_listbox = tk.Listbox(user_frame, width=16, font=("Arial", 10),
                                       relief=tk.RAISED, bd=2)
        self.user_listbox.pack(fill=tk.Y, expand=True)
        tk.Label(user_frame, text="Tipp: /w Name Text", font=("Arial", 8),
                 bg="#f0f0f0", fg="#9E9E9E").pack(pady=(5, 0))

        # Tipp-Anzeige ("X schreibt ...")
        self.typing_label = tk.Label(self.window, text="", font=("Arial", 9, "italic"),
                                     bg="#f0f0f0", fg="#9E9E9E", anchor="w")
        self.typing_label.pack(fill=tk.X, padx=15)

        # Eingabe
        input_frame = tk.Frame(self.window, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 8))
        self.input_field = tk.Entry(input_frame, font=("Arial", 12), relief=tk.RAISED,
                                    bd=2, bg="#ffffff")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message_action)
        self.input_field.bind("<Key>", self.on_typing)
        self.input_field.focus()
        tk.Button(input_frame, text="Senden", command=self.send_message_action,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  relief=tk.RAISED, bd=2, padx=20).pack(side=tk.RIGHT)

        # Button-Zeile
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        tk.Button(button_frame, text="🔄 Neu verbinden", command=self.connect,
                  bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, bd=2, padx=12).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(button_frame, text="🗑 Loeschen", command=self.clear_chat,
                  bg="#9E9E9E", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, bd=2, padx=12).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(button_frame, text="💾 Export", command=self.export_chat,
                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, bd=2, padx=12).pack(side=tk.LEFT)

    def set_status(self, verbunden):
        self.status_label.config(text="🟢 Verbunden" if verbunden else "🔴 Getrennt")

    def connect(self):
        if self.running:
            return
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

        # Private Nachricht?  Format: /w Name Text
        if text.startswith("/w "):
            teile = text[3:].split(" ", 1)
            if len(teile) < 2 or not teile[1].strip():
                self.display_message("❌ Format: /w <Name> <Text>", "system")
                return
            ziel, privat_text = teile[0], teile[1].strip()
            try:
                send_message(self.client_socket,
                             {"type": "private", "to": ziel, "text": privat_text})
                self.display_message(f"{zeitstempel()} 🔒 an {ziel}: {privat_text}", "private")
                self.input_field.delete(0, tk.END)
            except OSError:
                self.set_status(False)
                self.running = False
                self.display_message("❌ Senden fehlgeschlagen.", "system")
            return

        # Normale Nachricht
        try:
            send_message(self.client_socket, {"type": "chat", "text": text})
            self.display_message(f"{zeitstempel()} Du: {text}", "own")
            self.input_field.delete(0, tk.END)
        except OSError:
            self.set_status(False)
            self.running = False
            self.display_message("❌ Senden fehlgeschlagen (Verbindung weg).", "system")

    def on_typing(self, event=None):
        """Sendet einen Tipp-Hinweis - aber gedrosselt (hoechstens alle 2 Sekunden)."""
        if not self.running or self.typing_gesendet:
            return
        try:
            send_message(self.client_socket, {"type": "typing"})
            self.typing_gesendet = True
            # Drossel nach 2 Sekunden zuruecksetzen
            self.window.after(2000, self.reset_typing)
        except OSError:
            pass

    def reset_typing(self):
        self.typing_gesendet = False

    def receive_loop(self):
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
        try:
            while True:
                msg = self.incoming.get_nowait()
                self.handle_incoming(msg)
        except queue.Empty:
            pass
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
        elif typ == "private":
            zeile = f"{msg.get('time', '')} 🔒 von {msg.get('from', '?')}: {msg.get('text', '')}"
            self.display_message(zeile, "private")
        elif typ == "history":
            self.display_message("----- Bisheriger Verlauf -----", "system")
            for alt in msg.get("messages", []):
                zeile = f"{alt.get('time', '')} {alt.get('username', '?')}: {alt.get('text', '')}"
                self.display_message(zeile, "other")
            self.display_message("----- Neue Nachrichten -----", "system")
        elif typ == "typing":
            self.zeige_typing(msg.get("username", "Jemand"))
        elif typ == "_disconnect":
            self.running = False
            self.set_status(False)
            self.user_listbox.delete(0, tk.END)
            self.display_message("🔴 Verbindung zum Server verloren.", "system")

    def zeige_typing(self, name):
        """Zeigt kurz 'X schreibt ...' und blendet es nach 3 Sekunden aus."""
        self.typing_label.config(text=f"✍️  {name} schreibt ...")
        self.window.after(3000, lambda: self.typing_label.config(text=""))

    def update_userlist(self, users):
        self.user_listbox.delete(0, tk.END)
        for user in users:
            self.user_listbox.insert(tk.END, f"• {user}")

    def clear_chat(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def export_chat(self):
        """Speichert den aktuellen Chatverlauf als Textdatei."""
        inhalt = self.chat_area.get(1.0, tk.END).strip()
        if not inhalt:
            messagebox.showinfo("Export", "Der Chat ist leer.")
            return
        pfad = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textdatei", "*.txt")],
            title="Chat exportieren",
        )
        if pfad:
            try:
                with open(pfad, "w", encoding=ENCODING) as f:
                    f.write(inhalt)
                messagebox.showinfo("Export", f"Chat gespeichert:\n{pfad}")
            except OSError as e:
                messagebox.showerror("Export", f"Fehler beim Speichern:\n{e}")

    def on_close(self):
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
    print("  📨 MessengerService - Schritt 5 (Finale Version)")
    print("=" * 55)
    print("Starte in mehreren TERMINALS:")
    print()
    print("  Terminal 1 (Server):  python messenger_step5_final.py server")
    print("  Terminal 2 (Client):  python messenger_step5_final.py client")
    print("  Terminal 3 (Client):  python messenger_step5_final.py client")
    print()
    print("💡 Private Nachricht im Client:  /w <Name> <Text>")
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
