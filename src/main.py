import signal
import sys

from config import settings

from server import Server
from client import client


def main():
    server_config = settings["server.config"]
    host: str = server_config.get("Host", "127.0.0.1")
    port: int = (
        int(server_config.get("Port", "1234"))
        if len(sys.argv) == 1
        else int(sys.argv[1])
    )

    address: tuple[str, int] = (host, port)

    server = Server(address, client)
    server.start()

    # Can't pass variables into signal handlers
    def sigint_handler(signum, frame):
        print("Shutting down...")
        client.disconnect()
        server.stop()
        server.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    # For local testing only
    h = input()
    p = int(input())

    location = (h, p)

    client.connect_to_peer(location)


if __name__ == "__main__":
    main()
