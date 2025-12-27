import socket
import threading

from peer import listen_for_connections

class Server(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.listening = None

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        server.bind(address)
        server.listen()

    def run(self):
        self.listening = True
        while self.listening:
            listen_for_connections(self._socket)

    def stop(self):
        self.listening = False
