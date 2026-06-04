import sys
import signal
import argparse

from config import settings

from server import Server
from client import client


def main():
    server_config = settings["server.config"]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Port number to serve to",
        default=int(server_config.get("Port", "1234")),
    )
    parser.add_argument(
        "-n",
        "--hostname",
        type=str,
        help="Hostname to serve to",
        default=server_config.get("Host", "127.0.0.1"),
    )

    args = parser.parse_args()

    address: tuple[str, int] = (args.hostname, args.port)

    server = Server(address, client)
    server.start()

    # Can't pass variables into signal handlers
    def sigint_handler(signum, frame):
        print("\n[Main Thread] Shutting down...")
        client.disconnect()
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    # For local testing only
    h = "127.0.0.1"
    p = int(input("[Host <--> Peer] Enter peer port: "))

    location = (h, p)

    client.connect_to_peer(location)


if __name__ == "__main__":
    main()
