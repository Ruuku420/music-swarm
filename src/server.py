import socket
import threading

from connection import listen_for_connections

class Server(threading.Thread):
    def __init__(self, address, client):
        threading.Thread.__init__(self)
        self.listening = None
        self.client = client

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    def run(self):
        self._socket.bind(address)
        self._socket.listen()

        self.listening = True
        while self.listening:
            listen_for_connections(self._socket, self.client)

    def stop(self):
        self.listening = False
