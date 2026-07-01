"""
Schritt 1: Socket-Grundlagen - Echo-Server + CLI-Client (eine Verbindung)

Ziel: Die absoluten Grundlagen der Netzwerk-Programmierung mit TCP-Sockets lernen.
Alles laeuft LOKAL auf 127.0.0.1 (localhost) - kein Internet, kein externes Netzwerk.

So startest du diesen Schritt (zwei Terminals):
    Terminal 1 (Server):  python messenger_step1.py server
    Terminal 2 (Client):  python messenger_step1.py client

Der Server nimmt EINE Verbindung an und schickt jede Nachricht in GROSSBUCHSTABEN
zurueck (Echo). Mit 'quit' beendet der Client.
"""

import socket
import sys

# ---------------------------------------------------------------------------
# Gemeinsame Konstanten (in jedem Schritt oben in der Datei)
# ---------------------------------------------------------------------------
HOST = "127.0.0.1"   # localhost -> kein Internet, keine Windows-Firewall-Abfrage
PORT = 50007         # freier Port; bei "Port belegt" hier einfach aendern
ENCODING = "utf-8"   # wichtig fuer Umlaute (aeoeue) und Emojis

# Windows-Konsole auf UTF-8 umstellen, damit Emojis/Umlaute nicht abstuerzen
try:
    sys.stdout.reconfigure(encoding=ENCODING)
except Exception:
    pass


class MessengerServer:
    """Ein ganz einfacher Echo-Server: nimmt eine Verbindung an und antwortet."""

    def __init__(self):
        self.server_socket = None

    def start(self):
        # 1) Socket erstellen: AF_INET = IPv4, SOCK_STREAM = TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SO_REUSEADDR: Port sofort wieder benutzbar, ohne Wartezeit nach Neustart
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # 2) An Adresse + Port binden
            self.server_socket.bind((HOST, PORT))
            # 3) Auf Verbindungen lauschen (1 = Warteschlangen-Groesse)
            self.server_socket.listen(1)
            # Timeout: sonst blockiert accept()/recv() und Strg+C wuerde unter
            # Windows nie ankommen. So brechen die Aufrufe jede Sekunde kurz ab.
            self.server_socket.settimeout(1.0)
            print(f"🟢 Server laeuft auf {HOST}:{PORT}")
            print("⏳ Warte auf eine Verbindung...")

            # 4) Auf einen Client warten (accept bricht per Timeout ab -> Strg+C moeglich)
            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    break
                except socket.timeout:
                    continue
            print(f"✅ Verbunden mit {addr}")

            # 5) Nachrichten empfangen und als Echo zurueckschicken
            conn.settimeout(1.0)  # auch recv() unterbrechbar machen (Strg+C)
            with conn:
                while True:
                    try:
                        # recv() blockiert (max. 1 Sekunde), bis Daten ankommen
                        data = conn.recv(1024)
                    except socket.timeout:
                        continue  # keine Daten -> weiter warten (Strg+C wurde geprueft)

                    # Leere Bytes = der Client hat die Verbindung getrennt
                    if not data:
                        print("🔴 Client hat die Verbindung getrennt.")
                        break

                    nachricht = data.decode(ENCODING).strip()
                    print(f"📩 Empfangen: {nachricht}")

                    # Echo: gleiche Nachricht in Grossbuchstaben zurueck
                    antwort = nachricht.upper()
                    conn.sendall(antwort.encode(ENCODING))

        except OSError as e:
            print(f"❌ Server-Fehler: {e}")
            print(f"💡 Tipp: Ist Port {PORT} belegt? Aendere die Konstante PORT oder warte kurz.")
        except KeyboardInterrupt:
            print("\n👋 Server wird beendet (Strg+C).")
        finally:
            # Listening-Socket immer sauber schliessen
            if self.server_socket:
                self.server_socket.close()


class MessengerClient:
    """Ein einfacher CLI-Client: sendet Zeilen und zeigt das Echo an."""

    def __init__(self):
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Verbindung zum Server aufbauen
            self.client_socket.connect((HOST, PORT))
            print(f"✅ Mit Server {HOST}:{PORT} verbunden.")
            print("💬 Tippe eine Nachricht (oder 'quit' zum Beenden):")

            while True:
                nachricht = input("Du: ").strip()

                if nachricht.lower() == "quit":
                    print("👋 Verbindung wird getrennt.")
                    break

                if not nachricht:
                    continue

                # Nachricht senden
                self.client_socket.sendall(nachricht.encode(ENCODING))

                # Auf Echo-Antwort warten
                data = self.client_socket.recv(1024)
                if not data:
                    print("🔴 Server hat die Verbindung geschlossen.")
                    break

                print(f"Server (Echo): {data.decode(ENCODING)}")

        except ConnectionRefusedError:
            print("❌ Verbindung abgelehnt. Laeuft der Server schon?")
            print("💡 Starte zuerst: python messenger_step1.py server")
        except KeyboardInterrupt:
            print("\n👋 Client wird beendet (Strg+C).")
        finally:
            if self.client_socket:
                self.client_socket.close()


def print_usage():
    """Zeigt, wie das Programm gestartet wird (fuer Doppelklick-Nutzer)."""
    print("=" * 55)
    print("  📨 MessengerService - Schritt 1 (Echo-Server)")
    print("=" * 55)
    print("Starte das Programm in einem TERMINAL mit einem Modus:")
    print()
    print("  Terminal 1 (Server):  python messenger_step1.py server")
    print("  Terminal 2 (Client):  python messenger_step1.py client")
    print()
    print("=" * 55)


# Hauptprogramm
if __name__ == "__main__":
    # Modus aus dem Kommandozeilen-Argument lesen
    modus = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if modus == "server":
        MessengerServer().start()
    elif modus == "client":
        MessengerClient().start()
    else:
        print_usage()
        input("Druecke Enter zum Beenden...")
