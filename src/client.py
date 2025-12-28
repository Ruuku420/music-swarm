import socket
import threading

from peer import Peer
from connection import Connection


class Client:
    def __init__(self):
        self.peers = ()
        self.peers_lock = threading.RLock()

    def connect_to_peer(peer):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Server and client must use the same address
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        incoming = Connection(sock, peer.id_)
        peer.incoming_socket = incoming

    def add_peer(self, address, incomimg=None, outgoing=None):
        with self.peers_lock:
            new_peer = Peer(address)
            if new_peer in self.peer_list:
                return

            new_peer.incoming_socket = incomimg
            new_peer.outgoing_socket = outgoing

            self.peers.push(new_peer)

    def peers_from_list(self, peer_list):
        with self.peers_lock:
            for peer in peer_list:
                self.peers.push(peer)
