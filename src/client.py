import socket
import threading

from peer import Peer
from connection import Connection


class Client:
    def __init__(self):
        self.peers = []
        self.peers_lock = threading.RLock()

    def _connect(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)

        return Connection(sock, address)

    def connect_to_peer(self, address):
        conn = self.connect(address)
        conn.start()
        self.add_peer(address, conn)

    def add_peer(self, address, connection):
        new_peer = Peer(address)

        new_peer.connection = connection
        self.peers.append(new_peer)
        return new_peer

    def peers_from_list(self, addr_list):
        with self.peers_lock:
            for address in addr_list:
                self.connect_to_peer(address)

    def disconnect(self):
        with self.peers_lock:
            for peer in self.peers:
                peer.disconnect()
                self.peers.remove(peer)
