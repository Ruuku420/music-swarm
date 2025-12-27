import threading
import time

from packet_handler import PacketHeader, packetHandler

RECONNECT_RETRIES = 3
RECONNECT_TIMEOUT = 10

"""
TODO: This creates two peers on different threads from the same address
Replace the threading on peer for a thread on a incoming and outgoing SRI
"""

class Peer(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self._socket = socket
        self.address = address
        self.alive = True

    def run(self):
        while self.alive:
            self.read()

        self._close_connection();

    def _close_connection():
        self._socket.close()

    def send(self, packet):
        packetID = packetHandler.class_to_id[packet.__class__]
        packetHeader = PacketHeader(packetID)

        data = bytearray()
        data.extend(packetHeader.to_bytes())
        data.extend(packet.to_bytes())

        self._socket.sendall(data)  # Get OS error if sent to a dead socket

    def read(self):
        data = self._socket.recv(4096)

        if not data:
            self.alive = False
            return

        header = data[PacketHeader.PACKET_HEADER_SIZE - 1]
        packetHeader = PacketHeader()
        packetHeader.from_bytes(header)
        if packetHeader.id not in packetHeader.id_to_class.keys():
            return

        payload = data[PacketHeader.PACKET_HEADER_SIZE :]
        packet = packetHandler.id_to_class[packetHeader.id]()
        packet.from_bytes(payload)
        packet.handle(self)

def listen_for_connection(server):
    sock, addr = server.accept()
    peer = Peer(sock, addr)
    peer.start()
