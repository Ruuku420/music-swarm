import socket
import threading

from connection import listen_for_peer

# Maybe there is a better place to put this
from packet_handler import packetHandler

from packets.pex import PEXPacket
from packets.ping import PingPacket

packetHandler.registerPacket(PingPacket)
packetHandler.registerPacket(PEXPacket)


class Server(threading.Thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.daemon = True

        self.address = address
        self.listening = None
        self.client = client
        self._running = False

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self._running = True

        try:
            self._socket.bind(self.address)
        except OSError:
            print(f"\n[Server Thread] Could not bind to '{self.address[0]}:{self.address[1]}'.")
            print(f"\n[Server Thread] Perhaps try another port?")
            port = int(input("[Server Thread] Enter new host port: "))
            self.address = (self.address[0], port)
            self._socket.bind(self.address)


        self._socket.listen()
        print(f"\n[Server Thread] Now listening @ '{self.address[0]}:{self.address[1]}'!")

        while self._running:
            try:
                listen_for_peer(self._socket, self.client)
            except OSError:
                print(f"\n[Server Thread] Shutting down...")
                break

    def stop(self):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"\n[Server Thread] Error during shutdown: '{e}'")
        self._socket.close()
        self.join()
