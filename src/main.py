import signal
import sys

from config import settings

from server import Server
from client import Client


client = Client()


def sigint_handler(signum, frame):
    print("Shutting down...")
    client.disconnect()
    sys.exit(0)


def main():
    server_config = settings["server.config"]
    host: str = server_config.get("Host", "127.0.0.1")
    port: int = (
        int(server_config.get("Port", "1234"))
        if len(sys.argv) == 1
        else int(sys.argv[1])
    )

    address: tuple[str, int] = (host, port)

    signal.signal(signal.SIGINT, sigint_handler)

    server = Server(address, client)
    server.start()

    h = input()
    p = int(input())
    client.connect_to_peer((h, p))


if __name__ == "__main__":
    main()
