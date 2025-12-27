import socket

class Client:
    def __init__(self):
        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect_to_new_peers(self, peer_list):
        raise NotImplemented
