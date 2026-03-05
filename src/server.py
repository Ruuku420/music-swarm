import socket
import threading

from connection import listen_for_peer

# Maybe there is a better place to put this
from packet_handler import packetHandler

from packets.pex import PEXPacket
from packets.ping import PingPacket

packetHandler.registerPacket(PEXPacket)
packetHandler.registerPacket(PingPacket)


class Server(threading.Thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.address = address
        self.listening = None
        self.client = client

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    def run(self):
        self._socket.bind(self.address)
        self._socket.listen()
        while True:
            listen_for_peer(self._socket, self.client)

    def stop(self):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self._socket.close()
