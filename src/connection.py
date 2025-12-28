import threading

from packet_handler import PacketHeader, packetHandler

class Connection(threading.Thread):
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

        self._socket.sendall(data) # Get OS error if sent to a dead socket

    def read(self):
        # This byte size is completely arbitrary and has no real reason for being this way
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

def listen_for_connection(server, client):
    sock, addr = server.accept()
    connection = Connection(sock, addr)
    connection.start()
    client.add_peer(addr)

