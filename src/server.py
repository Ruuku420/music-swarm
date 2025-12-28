import socket
import threading

from connection import listen_for_peer


class Server(threading.Thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.address = address
        self.listening = None
        self.client = client

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    def run(self):
        self._socket.bind(self.address)
        self._socket.listen()

        self.listening = True
        while self.listening:
            listen_for_peer(self._socket, self.client)

    def stop(self):
        self.listening = False
