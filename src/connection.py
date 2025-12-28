import threading

from queue import Queue

from packet_handler import PacketHeader, packetHandler


class Connection(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self._socket = socket
        self._recieved_queue = Queue()
        self.address = address
        self.alive = True

    def run(self):
        while self.alive:
            self.read()

        self._close_connection()

    def _close_connection(self):
        self._socket.close()

    def send(self, packet):
        # socket.sendfile
        # Need to indicate packet length
        packetID = packetHandler.class_to_id[packet.__class__]  # FIXME
        packetHeader = PacketHeader(packetID)

        data = bytearray()
        data.extend(packetHeader.to_bytes())
        data.extend(packet.to_bytes())

        self._socket.sendall(data)  # Get OS error if sent to a dead socket

    def read(self):
        # TODO: Will break on any packets larger enough
        # This byte size is completely arbitrary
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
        packet = packetHandler.id_to_class[
            packetHeader.packet_id
        ]()  # FIXME: Enum issue

        packet.from_bytes(payload)
        packet.handle(self)


def listen_for_peer(server, client):
    incoming_sock, addr = server.accept()

    incoming_conn = Connection(incoming_sock, addr)
    incoming_conn.start()

    outgoing_sock = client.connect_to_outgoing(addr)
    outgoing_conn = Connection(outgoing_sock, addr)
    outgoing_conn.start()

    client.add_peer(addr, incoming=incoming_conn, outgoing=outgoing_conn)
