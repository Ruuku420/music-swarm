import sys

from server import Server
from client import Client

def main():
    host = '127.0.0.1'
    port = 1234 if len(sys.argv) == 1 else int(sys.argv[1])
    address = (host, port)

    server = Server(address)
    server.start()

    client = Client()

if __name__ == "__main__":
    main()
