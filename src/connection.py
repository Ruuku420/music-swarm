import threading

import packet_handler as Packet


class Connection(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self._socket = socket
        self.address = address
        self.alive = True

        self.RECV_BYTES = 4096

    def run(self):
        while self.alive:
            try:
                self.read()
            except RuntimeError:
                self.alive = False

        self._close_connection()

    def _close_connection(self):
        self._socket.close()

    def send(self, packet):
        # socket.sendfile

        # encode()
        # Need to indicate packet length
        packetID = Packet.packetHandler.class_to_id[packet.__class__]
        packetHeader = Packet.PacketHeader(packetID)

        packetTrailer = Packet.PacketTrailer()

        data = Packet.encode(header=packetHeader, payload=packet, trailer=packetTrailer)

        self._socket.sendall(data)  # Get OS error if sent to a dead socket

    def _check_for_sock_end(self, data):
        if not data:
            raise RuntimeError("Socket connection has been broken")
        else:
            return

    def read(self):
        # Localizing common heavy functions can majorly increase performance
        recv = self._socket.recv

        header_bytes = recv(Packet.PacketHeader.PACKET_HEADER_SIZE)
        self._check_for_sock_end(header_bytes)

        header = Packet.PacketHeader.from_bytes(header_bytes)
        packet_class = Packet.packetHandler.id_to_class.get(header.packet_id)
        if packet_class is None:
            raise RuntimeError("PacketID not valid")

        remaining = header.packet_length
        chunks = []

        while remaining > 0:
            chunk = recv(min(self.RECV_BYTES, remaining))
            self._check_for_sock_end(chunk)
            chunks.append(chunk)
            remaining -= len(chunk)

        payload = b"".join(chunks)

        trailer_bytes = recv(Packet.PacketTrailer.PACKET_TRAILER_SIZE)
        self._check_for_sock_end(trailer_bytes)
        trailer = Packet.PacketTrailer.from_bytes(trailer_bytes)
        trailer.verify(payload)

        packet = packet_class.from_bytes(payload)  # FIXME: Enum issue
        # Verify checksum before handling
        # Next based wrapper for handling?
        packet.handle(self)


def listen_for_peer(server, client):
    incoming_sock, addr = server.accept()

    incoming_conn = Connection(incoming_sock, addr)
    incoming_conn.start()

    outgoing_sock = client.connect_to_outgoing(addr)
    outgoing_conn = Connection(outgoing_sock, addr)
    outgoing_conn.start()

    client.add_peer(addr, incoming=incoming_conn, outgoing=outgoing_conn)
