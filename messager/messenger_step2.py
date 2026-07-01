"""
Schritt 2: Multi-Client CLI-Chat - Thread-per-Client + Broadcast + JSON-Protokoll

Ziel: Aus dem Echo-Server wird ein echter Chat-Server "in der Mitte".
Mehrere Clients koennen sich verbinden; eine Nachricht von A wird an ALLE
anderen weitergeleitet (Broadcast).

Neu in diesem Schritt:
- threading: pro Client ein eigener Thread (damit mehrere gleichzeitig gehen)
- threading.Lock: schuetzt die gemeinsame Client-Liste
- json-Protokoll mit Newline-Framing (siehe send_message / receive_messages)

So startest du diesen Schritt (drei Terminals):
    Terminal 1 (Server):  python messenger_step2.py server
    Terminal 2 (Client):  python messenger_step2.py client
    Terminal 3 (Client):  python messenger_step2.py client
"""

import socket
import sys
import json
import threading

HOST = "127.0.0.1"   # localhost -> kein Internet, keine Windows-Firewall-Abfrage
PORT = 50007         # bei "Port belegt" hier aendern
ENCODING = "utf-8"   # wichtig fuer Umlaute und Emojis

# Windows-Konsole auf UTF-8 umstellen, damit Emojis/Umlaute nicht abstuerzen
try:
    sys.stdout.reconfigure(encoding=ENCODING)
except Exception:
    pass


# ---------------------------------------------------------------------------
# Framing-Helfer: newline-getrenntes JSON
#
# WICHTIG: TCP ist ein Byte-STROM ohne Nachrichtengrenzen. Ein recv() kann
# mehrere Nachrichten zusammen oder eine Nachricht in Stuecken liefern.
# Loesung: Jede Nachricht ist ein JSON-Objekt, gefolgt von "\n". Der Empfaenger
# sammelt in einem Puffer und teilt bei jedem "\n" eine vollstaendige Nachricht ab.
# ---------------------------------------------------------------------------
def send_message(sock, message_dict):
    """Wandelt ein dict in JSON + '\\n' um und sendet es."""
    daten = (json.dumps(message_dict) + "\n").encode(ENCODING)
    sock.sendall(daten)


def receive_messages(sock, buffer):
    """
    Liest neue Bytes, haengt sie an 'buffer' an und gibt
    (liste_vollstaendiger_nachrichten, neuer_buffer) zurueck.
    Ist die Liste leer und buffer unveraendert -> Verbindung getrennt.
    """
    daten = sock.recv(4096)
    if not daten:
        return None, buffer  # None signalisiert: Verbindung geschlossen

    buffer += daten.decode(ENCODING)
    nachrichten = []

    # Alle vollstaendigen Zeilen (bis zum letzten "\n") abtrennen
    while "\n" in buffer:
        zeile, buffer = buffer.split("\n", 1)
        if zeile.strip():
            nachrichten.append(json.loads(zeile))

    return nachrichten, buffer


class MessengerServer:
    """Chat-Server: nimmt viele Clients an und verteilt Nachrichten (Broadcast)."""

    def __init__(self):
        self.server_socket = None
        self.clients = []                 # Liste der verbundenen Sockets
        self.lock = threading.Lock()      # schuetzt self.clients

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            # Timeout: accept() bricht jede Sekunde kurz ab, damit Strg+C funktioniert
            # (sonst blockiert accept() und das Signal kommt unter Windows nie an)
            self.server_socket.settimeout(1.0)
            print(f"🟢 Chat-Server laeuft auf {HOST}:{PORT}")
            print("⏳ Warte auf Clients... (Strg+C zum Beenden)")

            # Endlosschleife: immer wieder neue Clients annehmen
            while True:
                try:
                    conn, addr = self.server_socket.accept()
                except socket.timeout:
                    continue  # kein Client -> weiter warten (Strg+C wurde geprueft)

                with self.lock:
                    self.clients.append(conn)
                print(f"✅ Neuer Client verbunden: {addr} (aktiv: {len(self.clients)})")

                # Fuer jeden Client ein eigener Thread
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()

        except OSError as e:
            print(f"❌ Server-Fehler: {e}")
            print(f"💡 Tipp: Ist Port {PORT} belegt? Aendere PORT oder warte kurz.")
        except KeyboardInterrupt:
            print("\n👋 Server wird beendet.")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, conn, addr):
        """Laeuft in einem eigenen Thread: empfaengt Nachrichten dieses Clients."""
        buffer = ""
        try:
            while True:
                nachrichten, buffer = receive_messages(conn, buffer)
                if nachrichten is None:
                    break  # Client hat sauber getrennt

                for msg in nachrichten:
                    text = msg.get("text", "")
                    print(f"📩 {addr}: {text}")
                    # Weiterleiten an alle ANDEREN Clients
                    self.broadcast(msg, exclude=conn)

        except (ConnectionResetError, OSError):
            # Client hart getrennt (z. B. Fenster geschlossen)
            pass
        finally:
            self.remove_client(conn)
            print(f"🔴 Client getrennt: {addr} (aktiv: {len(self.clients)})")

    def broadcast(self, message_dict, exclude=None):
        """Sendet eine Nachricht an alle Clients (ausser 'exclude')."""
        with self.lock:
            # Kopie der Liste, damit wir sicher iterieren koennen
            for client in list(self.clients):
                if client is exclude:
                    continue
                try:
                    send_message(client, message_dict)
                except OSError:
                    # Toter Socket - stoert den Rest nicht
                    pass

    def remove_client(self, conn):
        with self.lock:
            if conn in self.clients:
                self.clients.remove(conn)
        conn.close()


class MessengerClient:
    """CLI-Client: sendet Eingaben und zeigt Nachrichten der anderen an."""

    def __init__(self):
        self.client_socket = None
        self.running = True

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
            print(f"✅ Mit Chat-Server {HOST}:{PORT} verbunden.")
            print("💬 Tippe Nachrichten (oder 'quit' zum Beenden):")

            # Empfangs-Thread im Hintergrund (blockiert nicht die Eingabe)
            empfang = threading.Thread(target=self.receive_loop, daemon=True)
            empfang.start()

            # Haupt-Schleife: Eingaben lesen und senden
            while self.running:
                text = input()
                if text.lower() == "quit":
                    break
                if not text.strip():
                    continue
                send_message(self.client_socket, {"type": "chat", "text": text})

        except ConnectionRefusedError:
            print("❌ Verbindung abgelehnt. Laeuft der Server schon?")
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            self.client_socket.close()
            print("👋 Verbindung getrennt.")

    def receive_loop(self):
        """Zeigt eingehende Nachrichten der anderen Clients an."""
        buffer = ""
        try:
            while self.running:
                nachrichten, buffer = receive_messages(self.client_socket, buffer)
                if nachrichten is None:
                    print("\n🔴 Server hat die Verbindung geschlossen.")
                    self.running = False
                    break
                for msg in nachrichten:
                    print(f"Andere: {msg.get('text', '')}")
        except (ConnectionResetError, OSError):
            self.running = False


def print_usage():
    print("=" * 55)
    print("  📨 MessengerService - Schritt 2 (Multi-Client CLI)")
    print("=" * 55)
    print("Starte in mehreren TERMINALS:")
    print()
    print("  Terminal 1 (Server):  python messenger_step2.py server")
    print("  Terminal 2 (Client):  python messenger_step2.py client")
    print("  Terminal 3 (Client):  python messenger_step2.py client")
    print()
    print("=" * 55)


if __name__ == "__main__":
    modus = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if modus == "server":
        MessengerServer().start()
    elif modus == "client":
        MessengerClient().start()
    else:
        print_usage()
        input("Druecke Enter zum Beenden...")
