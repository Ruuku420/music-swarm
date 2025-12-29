import threading

# from queue import Queue

from packet_handler import PacketHeader, packetHandler


class Connection(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self._socket = socket
        # self._received_queue = Queue()
        self.address = address
        self.alive = True

        self.RECV_BYTES = 4096

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

        # Might be better to use socket.send
        # Cannot tell how much data was sent if an error occurs
        self._socket.sendall(data)  # Get OS error if sent to a dead socket

    def _check_for_sock_end(self, data):
        if not data:
            raise RuntimeError("Socket connection has been broken")
        else:
            return

    def read(self):
        """
        Bill Gates says, "abstraction layers are like condoms.
        You should wear at least three otherwise you're a terrorist"
            - Terry A. Davis
        """

        chunks = []
        bytes_received = 0

        chunk = self._socket.recv(self.RECV_BYTES)
        try:
            self._check_for_sock_end(chunk)
        except RuntimeError:
            self.alive = False
            return

        header = chunk[PacketHeader.PACKET_HEADER_SIZE - 1]
        packetHeader = PacketHeader()
        packetHeader.from_bytes(header)
        if packetHeader.packet_id not in packetHandler.id_to_class.keys():
            return

        body = chunk[PacketHeader.PACKET_HEADER_SIZE :]
        bytes_received += len(body)
        chunks.append(body)

        while bytes_received < packetHeader.packet_length:
            chunk = self._socket.recv(self.RECV_BYTES)
            try:
                self._check_for_sock_end(chunk)
            except RuntimeError:
                self.alive = False
                return

            bytes_received += len(chunk)
            chunks.append(chunk)

        payload = b"".join(chunks)

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
