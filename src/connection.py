import threading

import socket

from queue import Queue

import packet_handler as Packet


class Connection:
    def __init__(self, socket, address):
        self._socket = socket
        self._send_queue = Queue()
        self.address = address

        # self.warning_log = []

        self.RECV_BYTES = 4096

        self.reading_thread = threading.Thread(target=self._read_loop)
        self.sending_thread = threading.Thread(target=self._send_loop)

    def run(self):
        self.reading_thread.start()
        self.sending_thread.start()

    def _read_loop(self):
        while True:
            try:
                self.read()
            except RuntimeError:
                break

        self._close_connection()

    def _send_loop(self):
        while True:
            data = self._send_queue.get()
            if data is None:
                break
            self._send(data)

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

        data = Packet.encode(
            header=packetHeader, payload=packet, trailer=packetTrailer
        )

        self._send_queue.put(data)

    def _send(self, data):
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

    def disconnect(self):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass  # already closed

        self._send_queue.put(None)
        self.reading_thread.join()
        self.sending_thread.join()


def listen_for_peer(server, client):
    sock, addr = server.accept()

    conn = Connection(sock, addr)
    conn.run()
    peer = client.add_peer(addr, conn)
    with client.peers_lock:
        peer.send_pex(client.peers)
