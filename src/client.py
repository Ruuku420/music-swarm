import socket
import threading

from peer import Peer


class Client:
    def __init__(self):
        self.peers = set()
        self.peers_lock = threading.RLock()

    def connect_to_outgoing(addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Server and client must use the same address
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect(addr)
        return sock

    def add_peer(self, address, incomimg=None, outgoing=None):
        with self.peers_lock:
            new_peer = Peer(address)
            if new_peer in self.peer_list:
                return

            new_peer.incoming_socket = incomimg
            new_peer.outgoing_socket = outgoing

            self.peers.append(new_peer)

    def peers_from_list(self, peer_list):
        with self.peers_lock:
            for peer in peer_list:
                self.peers.append(peer)

    def check_for_addr_in_peer():
        raise NotImplementedError
