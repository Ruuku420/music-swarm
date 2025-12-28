from config import settings

from server import Server
from client import Client


def main():
    server_config = settings["server.config"]
    host: str = server_config.get("Host", "127.0.0.1")
    port: int = int(server_config.get("Port", "1234"))

    address: tuple[str, int] = (host, port)

    client = Client()

    server = Server(address, client)
    server.start()


if __name__ == "__main__":
    main()
