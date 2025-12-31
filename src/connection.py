import threading

import packet_handler as Packet


class Connection(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self._socket = socket
        self.address = address
        self.alive = True

        # self.error_log = []

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
        packet_bytes = packet.to_bytes()

        packetID = Packet.packetHandler.class_to_id[packet.__class__]
        packetLength = len(packet_bytes)
        packetHeader = Packet.PacketHeader(packetID, packetLength)

        packetTrailer = Packet.PacketTrailer()
        packetTrailer.create_crc(packet_bytes)

        data = Packet.encode(header=packetHeader, payload=packet, trailer=packetTrailer)

        self._socket.sendall(data)

    def _check_for_sock_end(self, data):
        if not data:
            raise RuntimeError("Socket connection has been broken")
        else:
            return

    def read(self):
        # Localizing common heavy functions can majorly increase performance
        recv = self._socket.recv

        header_bytes = recv(Packet.PACKET_HEADER_SIZE)
        self._check_for_sock_end(header_bytes)

        header = Packet.PacketHeader.from_bytes(header_bytes)
        packet_class = Packet.packetHandler.id_to_class.get(header.packet_id)
        if packet_class is None:
            return

        remaining = header.packet_length
        chunks = []

        while remaining > 0:
            chunk = recv(min(self.RECV_BYTES, remaining))
            self._check_for_sock_end(chunk)
            chunks.append(chunk)
            remaining -= len(chunk)

        payload = b"".join(chunks)

        trailer_bytes = recv(Packet.PACKET_TRAILER_SIZE)
        self._check_for_sock_end(trailer_bytes)
        trailer = Packet.PacketTrailer.from_bytes(trailer_bytes)

        try:
            trailer.verify(payload)
        except RuntimeError:
            return

        packet = packet_class.from_bytes(payload)
        packet.handle(self)


def listen_for_peer(server, client):
    incoming_sock, addr = server.accept()

    incoming_conn = Connection(incoming_sock, addr)
    incoming_conn.start()

    with client.peer_lock:
        if addr in client.peers:
            idx = client.peers.index(addr)
            client.peers[idx].incoming_conn = incoming_conn
            return

    outgoing_sock = client.connect_to_outgoing(addr)
    outgoing_conn = Connection(outgoing_sock, addr)
    outgoing_conn.start()

    client.add_peer(addr, incoming=incoming_conn, outgoing=outgoing_conn)
