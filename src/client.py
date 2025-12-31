import socket
import threading

from peer import Peer
from connection import Connection


class Client:
    def __init__(self):
        self.peers = []
        self.peers_lock = threading.RLock()

    def connect_to_outgoing(addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Server and client must use the same address
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect(addr)
        return sock

    def add_peer(self, address, *, incomimg=None, outgoing=None):
        with self.peers_lock:
            new_peer = Peer(address)

            new_peer.incoming_socket = incomimg
            new_peer.outgoing_socket = outgoing

            if new_peer in self.peer_list:
                return
            else:
                self.peers.append(new_peer)

    def peers_from_list(self, addr_list):
        with self.peers_lock:
            for addr in addr_list:
                outgoing_sock = self.connect_to_outgoing(addr)
                outgoing_conn = Connection(outgoing_sock, addr)
                outgoing_conn.start()

                self.add_peer(addr, outgoing=outgoing_conn)

    def disconnect(self):
        with self.peers_lock:
            for peer in self.peers:
                peer.disconnect()
