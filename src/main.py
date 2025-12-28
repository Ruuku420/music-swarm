from config import settings

from server import Server
from client import Client

def main():
    server_config = settings['server.config']
    host = server_config.get('Host', '127.0.0.1')
    port = int(server_config.get('Port', '1234'))

    address = (host, port)

    client = Client()

    server = Server(address, client)
    server.start()

if __name__ == "__main__":
    main()
